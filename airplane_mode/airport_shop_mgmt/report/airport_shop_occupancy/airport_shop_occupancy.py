# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt


import frappe

def execute(filters=None):
    data = []
    airports = frappe.get_all("Airport", pluck="name")
    for ap in airports:
        counts = frappe.db.sql("""
            SELECT
                SUM(1) as total,
                SUM(CASE WHEN status='Occupied' THEN 1 ELSE 0 END) as occupied,
                SUM(CASE WHEN status='Available' THEN 1 ELSE 0 END) as available
            FROM `tabAirport Shop` WHERE airport=%s
        """, ap, as_dict=True)[0]
        occ = 0
        if counts.total:
            occ = round((counts.occupied or 0) * 100.0 / counts.total, 2)
        data.append([ap, counts.total or 0, counts.occupied or 0, counts.available or 0, f"{occ}%"])
    columns = [
        {"label":"Airport","fieldname":"airport","fieldtype":"Link","options":"Airport","width":200},
        {"label":"Total","fieldname":"total","fieldtype":"Int","width":80},
        {"label":"Occupied","fieldname":"occupied","fieldtype":"Int","width":90},
        {"label":"Available","fieldname":"available","fieldtype":"Int","width":90},
        {"label":"Occupancy %","fieldname":"occ","fieldtype":"Data","width":110},
    ]
    return columns, [
        {"airport": r[0], "total": r[1], "occupied": r[2], "available": r[3], "occ": r[4]} for r in data
    ]
