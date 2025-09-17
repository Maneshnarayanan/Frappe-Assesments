frappe.listview_settings['Monthly Rent'] = {
    onload(listview) {
        listview.page.add_action_item(__('Send Reminder Email'), function() {
            let selected = listview.get_checked_items();

            if (!selected.length) {
                frappe.msgprint(__('Please select at least one Monthly Rent record.'));
                return;
            }

            frappe.call({
                method: "airplane_mode.airport_shop_mgmt.doctype.monthly_rent.monthly_rent.send_reminder_emails",
                args: {
                    rents: selected.map(d => d.name)
                },
                callback: function(r) {
                    if (!r.exc) {
                        frappe.msgprint(__('Reminder emails have been sent.'));
                        listview.refresh();
                    }
                }
            });
        });
    }
};

