import frappe
import random

def execute():
    # Fetch all airplane tickets that don't have a seat assigned
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ["is", "not set"]}, pluck="name")
    
    for ticket in tickets:
        seat_number = random.randint(1, 99)
        seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        seat = f"{seat_number}{seat_letter}"
        
        frappe.db.set_value("Airplane Ticket", ticket, "seat", seat)
