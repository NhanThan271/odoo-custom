import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const result = await super.validateOrder(isForceValidate);

        this.notification.add(
            "Đơn hàng đã thanh toán thành công",
            {
                type: "success",
                className: "custom-pos-notification",
            }
        );

        return result;
    },
});