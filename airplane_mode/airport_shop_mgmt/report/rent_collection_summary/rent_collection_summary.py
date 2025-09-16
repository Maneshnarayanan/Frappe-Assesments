# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Month", "fieldname": "billing_month", "fieldtype": "Data", "width": 120},
        {"label": "Tenant", "fieldname": "tenant", "fieldtype": "Link", "options": "Tenant", "width": 200},
        {"label": "Billed Amount", "fieldname": "billed", "fieldtype": "Currency", "width": 150},
        {"label": "Paid Amount", "fieldname": "paid", "fieldtype": "Currency", "width": 150},
        {"label": "Outstanding", "fieldname": "outstanding", "fieldtype": "Currency", "width": 150},
    ]

    conditions = []
    values = {}

    if filters.get("airport"):
        conditions.append("airport = %(airport)s")
        values["airport"] = filters["airport"]

    if filters.get("tenant"):
        conditions.append("tenant = %(tenant)s")
        values["tenant"] = filters["tenant"]

    if filters.get("from_month"):
        conditions.append("billing_month >= %(from_month)s")
        values["from_month"] = filters["from_month"]

    if filters.get("to_month"):
        conditions.append("billing_month <= %(to_month)s")
        values["to_month"] = filters["to_month"]

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    data = frappe.db.sql(f"""
        SELECT
            billing_month,
            tenant,
            SUM(amount) as billed,
            SUM(paid_amount) as paid,
            SUM(amount - paid_amount) as outstanding
        FROM `tabMonthly Rent`
        {where_clause}
        GROUP BY billing_month, tenant
        ORDER BY billing_month ASC, tenant ASC
    """, values, as_dict=True)

    return columns, data
