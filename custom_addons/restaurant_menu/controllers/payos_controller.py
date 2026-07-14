import hashlib
import hmac
import json
import logging
import random
import time

import requests
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class PayOSController(http.Controller):

    PAYOS_CLIENT_ID = "d52a431e-b4c6-4d29-884c-b0557caa196a"
    PAYOS_API_KEY = "50a8e984-4e6d-4133-b8f9-c89308ba619c"
    PAYOS_CHECKSUM_KEY = "bd9a87d8dd769f3221dde8b4c2c77920f2af8d52eadced82b6871db27b869678"
    PAYOS_BASE_URL = "https://api-merchant.payos.vn"

    def _sign_payment_request(self, checksum_key, data):

        raw = "&".join(
            f"{k}={data[k]}"
            for k in ["amount", "cancelUrl", "description", "orderCode", "returnUrl"]
        )
        return hmac.new(
            checksum_key.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def _verify_webhook_signature(self, checksum_key, webhook_data):
        
        data = webhook_data.get("data", {})
        sorted_keys = sorted(data.keys())
        raw = "&".join(f"{k}={data.get(k) if data.get(k) is not None else ''}" for k in sorted_keys)
        expected = hmac.new(
            checksum_key.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, webhook_data.get("signature", ""))

    @http.route("/pos_payos/create_payment", type="json", auth="user")
    def create_payment(self, payment_method_id, amount, order_reference):
        pm = request.env["pos.payment.method"].sudo().browse(int(payment_method_id))

        order_code = int(f"{int(time.time())}{random.randint(100,999)}")
        amount_int = int(round(amount))

        base_url = request.httprequest.url_root.rstrip("/")
        payload = {
            "orderCode": order_code,
            "amount": amount_int,
            "description": order_reference[:25],
            "returnUrl": f"{base_url}/pos_payos/return",
            "cancelUrl": f"{base_url}/pos_payos/cancel",
        }
        payload["signature"] = self._sign_payment_request(
            self.PAYOS_CHECKSUM_KEY,
            payload
        )

        try:
            resp = requests.post(
                f"{self.PAYOS_BASE_URL}/v2/payment-requests",
                json=payload,
                headers={
                    "x-client-id": self.PAYOS_CLIENT_ID,
                    "x-api-key": self.PAYOS_API_KEY,
                    "Content-Type": "application/json",
                },
                timeout=15,
            )
            resp.raise_for_status()
            result = resp.json()
        except requests.RequestException as e:
            _logger.error("PayOS create_payment failed: %s", e)
            return {"error": "Không thể tạo link thanh toán PayOS"}

        if result.get("code") != "00":
            _logger.error("PayOS trả lỗi: %s", result)
            return {"error": result.get("desc", "PayOS error")}

        data = result["data"]

        request.env["pos.payos.transaction"].sudo().create({
            "order_code": str(order_code),
            "payment_method_id": pm.id,
            "payment_link_id": data.get("paymentLinkId"),
            "amount": amount_int,
            "status": "pending",
        })

        return {
            "qrCode": data.get("qrCode"),
            "checkoutUrl": data.get("checkoutUrl"),
            "paymentLinkId": data.get("paymentLinkId"),
            "orderCode": order_code,
        }

    @http.route("/pos_payos/check_status", type="json", auth="user")
    def check_status(self, orderCode):

        txn = request.env["pos.payos.transaction"].sudo().search(
            [("order_code", "=", str(orderCode))],
            limit=1,
        )

        if not txn:
            return {"status": "pending"}

        try:

            resp = requests.get(
                f"{self.PAYOS_BASE_URL}/v2/payment-requests/{txn.payment_link_id}",
                headers={
                    "x-client-id": self.PAYOS_CLIENT_ID,
                    "x-api-key": self.PAYOS_API_KEY,
                },
                timeout=10,
            )

            resp.raise_for_status()

            result = resp.json()

            _logger.info("========== PAYOS ==========")
            _logger.info(result)

            if result.get("code") != "00":
                return {"status": txn.status}

            data = result.get("data", {})

            status = str(data.get("status", "")).upper()

            if status == "PAID":

                txn.write({
                    "status": "paid"
                })

                return {"status": "paid"}

            elif status in ("CANCELLED", "EXPIRED"):

                txn.write({
                    "status": "cancelled"
                })

                return {"status": "cancelled"}

            return {"status": "pending"}

        except Exception as e:

            _logger.exception(e)

            return {"status": "pending"}

    @http.route("/pos_payos/cancel_payment", type="json", auth="user")
    def cancel_payment(self, payment_method_id, orderCode):
        pm = request.env["pos.payment.method"].sudo().browse(int(payment_method_id))
        txn = request.env["pos.payos.transaction"].sudo().search(
            [("order_code", "=", str(orderCode))], limit=1
        )
        if not txn:
            return {"success": False}

        try:
            requests.post(
                f"{self.PAYOS_BASE_URL}/v2/payment-requests/{txn.payment_link_id}/cancel",
                json={},
                headers={
                    "x-client-id": self.PAYOS_CLIENT_ID,
                    "x-api-key": self.PAYOS_API_KEY,
                    "Content-Type": "application/json",
                },
                timeout=10,
            )
        except requests.RequestException as e:
            _logger.warning("PayOS cancel failed: %s", e)

        txn.status = "cancelled"
        return {"success": True}

    @http.route("/pos_payos/webhook", type="http", auth="public", csrf=False, methods=["POST"])
    def webhook(self):
        try:
            webhook_data = json.loads(request.httprequest.data)
        except ValueError:
            return Response(json.dumps({"error": "invalid json"}), content_type="application/json", status=400)

        pm = request.env["pos.payment.method"].sudo().search(
            [("use_payment_terminal", "=", "payos")], limit=1
        )
        if not self._verify_webhook_signature(
            self.PAYOS_CHECKSUM_KEY,
            webhook_data
        ):
            _logger.warning("PayOS webhook: chữ ký không hợp lệ")
            return Response(json.dumps({"error": "invalid signature"}), content_type="application/json", status=400)

        data = webhook_data.get("data", {})
        order_code = str(data.get("orderCode"))
        txn = request.env["pos.payos.transaction"].sudo().search(
            [("order_code", "=", order_code)], limit=1
        )
        if txn:
            txn.write({"status": "paid", "raw_webhook_data": json.dumps(webhook_data)})

        return Response(json.dumps({"success": True}), content_type="application/json")

    @http.route("/pos_payos/return", type="http", auth="public", csrf=False)
    def return_url(self, **kwargs):
        return request.render("web.login", {}) 

    @http.route("/pos_payos/cancel", type="http", auth="public", csrf=False)
    def cancel_url(self, **kwargs):
        return request.render("web.login", {})