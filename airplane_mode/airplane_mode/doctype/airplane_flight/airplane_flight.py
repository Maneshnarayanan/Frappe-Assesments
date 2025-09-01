
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
