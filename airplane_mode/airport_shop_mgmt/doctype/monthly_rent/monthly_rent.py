# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class MonthlyRent(Document):
    def validate(self):
        # keep status in sync
        if (self.paid_amount or 0) <= 0:
            self.status = "Unpaid"
        elif (self.paid_amount or 0) < (self.amount or 0):
            self.status = "Partially Paid"
        else:
            self.status = "Paid"

        if self.due_date and getdate(self.due_date) < getdate(self.period_end) and (self.amount or 0) > 0:
            pass  # acceptable; due date can be within or after period



@frappe.whitelist()
def send_reminder_emails(rents):
    if isinstance(rents, str):
        import json
        rents = json.loads(rents)

    settings = frappe.get_single("Airport Shop Settings")
    template = settings.default_email_template or \
        "Dear {{ tenant }},\n\nThis is a reminder that rent for {{ billing_month }} " \
        "amounting to {{ amount }} is due on {{ due_date }} for Shop {{ shop }} at {{ airport }}.\n\nThank you."

    for rent_name in rents:
        rent = frappe.get_doc("Monthly Rent", rent_name)
        tenant = frappe.get_doc("Tenant", rent.tenant)

        if not tenant.email_id:
            continue

        ctx = {
            "tenant": tenant.tenant_name,
            "billing_month": rent.billing_month,
            "amount": frappe.utils.fmt_money(rent.amount),
            "due_date": frappe.utils.formatdate(rent.due_date),
            "shop": rent.shop,
            "airport": rent.airport
        }
        msg = frappe.render_template(template, ctx)

        frappe.sendmail(
            recipients=[tenant.email_id],
            cc=[settings.cc_email] if settings.cc_email else None,
            subject=f"Rent Reminder: {rent.billing_month} - {rent.shop}",
            message=msg
        )

    return True
