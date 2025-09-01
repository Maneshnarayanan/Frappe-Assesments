// Copyright (c) 2025, maneshk27@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
    refresh: function (frm) {

        if (frm.doc.website && frm.doc.website.trim() !== "") {
            frm.add_web_link(frm.doc.website, "Official Website");
        }
    }
});
