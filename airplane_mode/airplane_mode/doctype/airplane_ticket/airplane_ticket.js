// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        frm.add_custom_button(__('Set Seat Number'), () => {
            let d = new frappe.ui.Dialog({
                title: 'Enter Seat Number',
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Set',
                primary_action(values) {
                    // Set the seat field in the form
                    frm.set_value('seat', values.seat_number);
                    d.hide();
                }
            });
            d.show();
        });
    }
});
