import frappe
 
def execute():
    default_types = ["Stall", "Walk-through", "Normal"]
 
    for shop_type in default_types:
        if not frappe.db.exists("Shop Type", {"name": shop_type}):
            doc = frappe.get_doc({
                "doctype": "Shop Type",
                "name": shop_type,
                "enabled": 1
            })
            doc.insert(ignore_permissions=True)