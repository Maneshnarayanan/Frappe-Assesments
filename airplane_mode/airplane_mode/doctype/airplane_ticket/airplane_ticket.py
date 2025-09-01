# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
import string

class AirplaneTicket(Document):

    def on_submit(self):
        if self.status != "Boarded":
            frappe.throw("Only tickets with status 'Boarded' can be submitted.")

    def validate(self):
       
     
        self.remove_duplicate_addons()
        self.calculate_total_amount()

    def before_insert(self):
         self.check_flight_availability()
         self.set_seat_number()    
    
    def remove_duplicate_addons(self):
            
            unique_items = {}
            new_add_ons = []
        
            for d in self.add_ons:
                if d.item not in unique_items:
                    unique_items[d.item] = d
                    new_add_ons.append(d)
                else:
                    frappe.msgprint(
                        f"Duplicate add-on '{d.item}' was removed.",
                        alert=True
                    )
        
            
            self.set("add_ons", new_add_ons)
    
    def calculate_total_amount(self):
           
            add_ons_total = sum([d.amount for d in self.add_ons])
            self.total_amount = (self.flight_price or 0) + add_ons_total
 
    def set_seat_number(self):
     
        seat_number = random.randint(1, 99)
      
        seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
      
        self.seat = f"{seat_number}{seat_letter}"

    def check_flight_availability(self):
        flight = frappe.get_doc("Airplane Flight", self.flight)
        count = frappe.db.count("Airplane Ticket", {"flight": self.flight, "status": not "Cancelled"})
        airplane = frappe.get_doc("Airplane", flight.airplane)
        if count >= airplane.capacity:
            frappe.throw("No seats available on this flight.")