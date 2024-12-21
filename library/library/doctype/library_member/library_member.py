# Copyright (c) 2024, Ayush Marhatta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):
    def before_save(self):
        names_map = {"Student": "student_name", "Instructor": "instructor_name", "Employee": "employee_name"}
        if self.library_member:
            self.full_name = frappe.db.get_value(self.member_type, self.library_member, names_map[self.member_type])
            self.first_name = self.full_name.split(" ")[0]
            self.last_name = self.full_name.split(" ")[-1]
        else:
        	self.full_name = f"{self.first_name} {self.last_name}"
