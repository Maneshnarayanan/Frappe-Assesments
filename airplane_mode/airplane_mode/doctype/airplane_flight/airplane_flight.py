
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



def enqueue_ticket_gate_update(doc, method):
    """Check if gate number changed, then enqueue background job"""
    # Fetch previous gate number from DB
    # old_gate = frappe.db.get_value("Airplane Flight", doc.name, "gate_number")
    # frappe.msgprint(f"Old gate: {old_gate}, New gate: {doc.gate_number}")
    # Only enqueue if gate number actually changed
  
    frappe.enqueue(
            "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gates_job",
            flight=doc.name,
            gate_number=doc.gate_number,
            queue="long",
            timeout=600
        )
    frappe.logger().info(f"Queued ticket gate update for flight {doc.name} (Gate {doc.gate_number})")



def update_ticket_gates_job(flight, gate_number):
    """Background job to update all tickets for a given flight"""
    tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight}, pluck="name")
    frappe.msgprint(f"Updating {len(tickets)} tickets for flight {flight} to gate {gate_number}")
    for ticket in tickets:
        frappe.db.set_value("Airplane Ticket", ticket, "gate_number", gate_number, update_modified=False)

    frappe.db.commit()
    frappe.logger().info(f"✅ Updated {len(tickets)} tickets for flight {flight} to gate {gate_number}")