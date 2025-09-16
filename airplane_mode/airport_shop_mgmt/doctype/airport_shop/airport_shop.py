# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt




import frappe
from frappe.model.document import Document

class AirportShop(Document):

    def on_update_after_submit(self):
        # Update counts whenever a submitted shop record is edited
        self.update_airport_counts()

    def on_submit(self):
        # Also update counts on first submission
        self.update_airport_counts()

    def on_cancel(self):
        # Update counts if shop is cancelled
        self.update_airport_counts()

    def update_airport_counts(self):
        if not self.airport:
            return

        total = frappe.db.count("Airport Shop", {"airport": self.airport, "docstatus": 1})
        occupied = frappe.db.count("Airport Shop", {"airport": self.airport, "status": "Occupied", "docstatus": 1})
        available = total - occupied

        frappe.db.set_value(
            "Airport",
            self.airport,
            {
                "total_shops": total,
                "occupied_shops": occupied,
                "available_shops": available
            },
            update_modified=False
        )


def get_context(context):
    filters = {"publish": 1}
    if frappe.form_dict.get("airport"):
        filters["airport"] = frappe.form_dict.get("airport")

    q = frappe.form_dict.get("q")
    if q:
        shops = frappe.get_all(
            "Airport Shop",
            filters=filters,
            or_filters={"shop_name": ["like", f"%{q}%"], "shop_number": ["like", f"%{q}%"]},
            fields=["name", "shop_name", "shop_number", "airport", "status", "shop_image", "area"],
            order_by="shop_name asc",
            limit_page_length=200,
        )
    else:
        shops = frappe.get_all(
            "Airport Shop",
            filters=filters,
            fields=["name", "shop_name", "shop_number", "airport", "status", "shop_image", "area"],
            order_by="shop_name asc",
            limit_page_length=200,
        )

    context.shops = shops
    context.q = q
    context.airport_filter = frappe.form_dict.get("airport")
    return context