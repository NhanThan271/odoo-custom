import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    async addProductToOrder(product) {
        await super.addProductToOrder(product);

        this.notification.add(
            `Đã thêm "${product.display_name}" vào đơn hàng`,
            {
                type: "success",
                sticky: false,
                className: "custom-pos-notification",
            }
        );
    },
});