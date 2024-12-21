// Copyright (c) 2024, Ayush Marhatta and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Member", {
	refresh(frm) {
		frm.add_custom_button("Create Membership", () => {
			frappe.new_doc("Library Membership", {
				library_member: frm.doc.name,
			});
		});
		frm.add_custom_button("Create Transaction", () => {
			frappe.new_doc("Library Transaction", {
				library_member: frm.doc.name,
			});
		});
	},
    member_type(frm) {
        frm.set_value("library_member", null);
    },
    library_member(frm) {
        frm.set_value("first_name", null);
        frm.set_value("last_name", null);
        frm.set_value("full_name", null);
    }
});
