
import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):

    def get_route(self):
        # This defines the URL route for the flight
        return f"flights/{self.name.lower().replace(' ', '-')}"
    
    def on_submit(self):
        self.status = "Completed"


def get_context(context):
    # This will automatically get the doc for the route
    context.no_cache = 1
    # `doc` is already injected by WebsiteGenerator
    flight = context.doc
    context.flight = flight
    return context



@frappe.whitelist()
def update_ticket_gates(flight, gate_number):
    """Background job to update gate numbers in all tickets of a flight"""
    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight}, pluck="name")

    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket, "gate_number", gate_number, update_modified=False)

    frappe.db.commit()
    frappe.logger().info(f"Updated {len(tickets)} tickets for flight {flight} to gate {gate_number}")
