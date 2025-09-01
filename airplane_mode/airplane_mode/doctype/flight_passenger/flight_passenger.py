# Copyright (c) 2025, maneshk27@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class FlightPassenger(Document):
     def before_save(self):
        first = self.first_name or ""
        last = self.last_name or ""
        # Always join both if available
        self.full_name = " ".join([first, last]).strip()