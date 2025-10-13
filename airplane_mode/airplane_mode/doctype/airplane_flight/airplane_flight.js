// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt
frappe.ui.form.on("Airplane Flight", {
    refresh(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Change Gate Number'), () => {
                let d = new frappe.ui.Dialog({
                    title: 'Change Gate Number',
                    fields: [
                        {
                            fieldname: 'new_gate',
                            fieldtype: 'Data',
                            label: 'New Gate Number',
                            reqd: 1
                        }
                    ],
                    primary_action_label: 'Update',
                    async primary_action(values) {
                        await frm.set_value('gate_number', values.new_gate);
                        await frm.save_or_update();
                        frappe.msgprint(__('Gate number updated to {0}. Ticket updates have been queued.', [values.new_gate]));
                        d.hide();
                    }
                });
                d.show();
            });
        }
    }
});

