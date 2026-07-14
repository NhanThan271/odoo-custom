import { patch } from "@web/core/utils/patch";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

patch(OrderSummary.prototype, {
    bookTable() {
        console.log("bookTable() PATCH ĐANG CHẠY");
        const table = this.pos.get_order().table_id;

        this.pos.get_order().setBooked(true);
        this.pos.showScreen("FloorScreen");

        if (table) {
            this.env.services.notification.add(
                `Đã đặt bàn ${table.table_number}`,
                {
                    type: "success",
                    className: "custom-pos-notification",
                }
            );
        }
    },
});