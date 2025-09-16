# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import add_days, get_first_day, get_last_day, nowdate

class LeaseContract(Document):
    def validate(self):
        shop = frappe.get_doc("Airport Shop", self.shop)
        if self.start_date >= self.end_date:
            frappe.throw("End Date must be after Start Date.")
        if self.is_new():
            if shop.status != "Available":
                frappe.throw(f"Shop {shop.name} is not available (status: {shop.status}).")
        # Pull airport from shop for consistency
        self.airport = shop.airport

    def on_submit(self):
        shop = frappe.get_doc("Airport Shop", self.shop)
        shop.status = "Occupied"
        shop.current_tenant = self.tenant
        shop.active_lease = self.name
        shop.save(ignore_permissions=True)
        # Optional: create current month's rent immediately
        from airplane_mode.airport_shop_mgmt.utils.rent import ensure_monthly_rent
        ensure_monthly_rent(self.name)

    def on_cancel(self):
        # free the shop if this was the active lease
        shop = frappe.get_doc("Airport Shop", self.shop)
        if shop.active_lease == self.name:
            shop.status = "Available"
            shop.current_tenant = None
            shop.active_lease = None
            shop.save(ignore_permissions=True)
