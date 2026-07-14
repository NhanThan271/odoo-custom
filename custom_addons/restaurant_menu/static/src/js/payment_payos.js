import { PaymentInterface } from "@point_of_sale/app/payment/payment_interface";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { PayOSQRPopup } from "@restaurant_menu/js/payos_popup";
import { register_payment_method } from "@point_of_sale/app/store/pos_store";

export class PaymentPayOS extends PaymentInterface {
    setup() {
        super.setup(...arguments);
        this.paymentLineResolvers = {};
    }

    pending_payos_line() {
        return this.pos.getPendingPaymentLine("payos");
    }

    async send_payment_request(uuid) {
        super.send_payment_request(uuid);
        const order = this.pos.get_order();

        const line = order.payment_ids.find(
            (paymentLine) => paymentLine.uuid === uuid
        );
        line.set_payment_status("waiting");

        const res = await rpc("/pos_payos/create_payment", {
            payment_method_id: this.payment_method_id.id,
            amount: line.amount,
            order_reference: order.name,
        });
        this.currentOrderCode = res.orderCode;

        this.showQRDialog(
            res.qrCode,
            line.amount
        );

        return await this.waitForPayment(res.orderCode);
    }

    async waitForPayment(orderCode) {
        return new Promise((resolve) => {
            const interval = setInterval(async () => {

                const res = await rpc("/pos_payos/check_status", {
                    orderCode,
                });

                const line = this.pending_payos_line();

                if (!line) {
                    clearInterval(interval);
                    resolve(false);
                    return;
                }

                if (res.status === "paid") {
                    clearInterval(interval);

                    this.dialogClose?.();

                    line.set_payment_status("done");

                    resolve(true);

                } else if (
                    res.status === "cancelled" ||
                    res.status === "expired"
                ) {

                    clearInterval(interval);

                    this.dialogClose?.();

                    order.remove_paymentline(line);

                    resolve(false);
                }

            }, 3000);
        });
    }

    async send_payment_cancel(order, uuid) {
        await rpc("/pos_payos/cancel_payment", {
            payment_method_id: this.payment_method_id.id,
            orderCode: this.currentOrderCode,
        });

        const line = order.payment_ids.find(l => l.uuid === uuid);
        if (line) {
            order.remove_paymentline(line);
        }

        this.dialogClose?.();

        return true;
    }

    showQRDialog(qrCode, amount) {
        const qrImageUrl = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(qrCode)}`;
        this.dialogClose = this.env.services.dialog.add(PayOSQRPopup, {
            title: "Thanh toán PayOS",
            qrImageUrl,
            formattedAmount: this.pos.env.utils.formatCurrency(amount),
            status: "waiting",
            close: () => this.dialogClose?.(),
        });
    }
}

register_payment_method(
    "payos",
    PaymentPayOS
);