# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt


import frappe

def execute(filters=None):
    # Fetch all airlines
    airlines = frappe.get_all("Airline", pluck="name")

    # Revenue aggregation grouped by flight
    revenues = frappe.db.get_all(
        "Airplane Ticket",
        fields=["flight", "SUM(total_amount) as revenue"],
        group_by="flight"
    )

    # Map flight -> revenue
    flight_revenue = {row.flight: row.revenue for row in revenues if row.flight}

    # Map airline -> revenue
    airline_revenue = {}
    for airline in airlines:
        # get airplanes of this airline
        airplanes = frappe.get_all("Airplane", filters={"airline": airline}, pluck="name")
        if not airplanes:
            airline_revenue[airline] = 0
            continue

        # get flights of these airplanes
        flights = frappe.get_all("Airplane Flight", filters={"airplane": ["in", airplanes]}, pluck="name")
        airline_revenue[airline] = sum(flight_revenue.get(f, 0) for f in flights)

    # Prepare rows
    data = []
    total = 0
    for airline in airlines:
        revenue = airline_revenue.get(airline, 0) or 0
        data.append({
            "airline": airline,
            "revenue": revenue
        })
        total += revenue

   
    data.sort(key=lambda d: (d["revenue"] == 0, -d["revenue"]))

    # Columns
    columns = [
        {"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]

    # Chart
    chart = {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [{"values": [d["revenue"] for d in data]}],
        },
        "type": "donut",
    }

    # Summary
    summary = [
        {"label": "Total Revenue", "value": total, "indicator": "Green"},
    ]

    return columns, data, None, chart, summary
