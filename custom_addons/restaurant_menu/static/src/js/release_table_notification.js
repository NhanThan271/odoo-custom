import { patch } from "@web/core/utils/patch";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

patch(OrderSummary.prototype, {
    async unbookTable() {
        const table = this.pos.selectedTable;
        const tableNumber = table?.table_number;

        await super.unbookTable(...arguments);

        if (tableNumber) {
            this.pos.env.services.notification.add(
                `Đã giải phóng bàn ${tableNumber}`,
                {
                    type: "success",
                    className: "custom-pos-notification",
                }
            );
        }
    },
});