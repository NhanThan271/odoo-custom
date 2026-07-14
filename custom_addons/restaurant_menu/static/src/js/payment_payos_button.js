/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    async onClickPayOS() {

        const order = this.currentOrder;

        const payosMethod =
            this.payment_methods_from_config.find(
                p => p.use_payment_terminal === "payos"
            );

        if (!payosMethod) {
            this.notification.add(
                "Chưa cấu hình PayOS",
                { type: "danger" }
            );
            return;
        }

        await this.addNewPaymentLine(payosMethod);

        const line = order.get_selected_paymentline();

        line.set_amount(order.get_due());

        await this.sendPaymentRequest(line);
    },
});