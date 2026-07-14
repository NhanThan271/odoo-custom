import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class PayOSQRPopup extends Component {
    static template = "restaurant_menu.PayOSQRPopup";
    static components = { Dialog };
    static props = {
        title: String,
        qrImageUrl: String,
        formattedAmount: String,
        status: String,
        close: Function,
    };
}