# Copyright (c) 2024, Ayush Marhatta and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.docstatus import Docstatus

class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            # set the book status to be Issued
            book = frappe.get_doc("Book", self.book)
            book.status = "Issued"
            book.save()

        elif self.type == "Return":
            self.validate_return()
            # set the book status to be Available
            book = frappe.get_doc("Book", self.book)
            book.status = "Available"
            book.save()

    def validate_issue(self):
        self.validate_membership()
        book = frappe.get_doc("Book", self.book)
        # book cannot be issued if it is already issued
        if book.status == "Issued":
            frappe.throw(_("book is already issued by another member"))

    def validate_return(self):
        book = frappe.get_doc("Book", self.book)
        # book cannot be returned if it is not issued first
        if book.status == "Available":
            frappe.throw(_("book cannot be returned without being issued first"))

    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<=", self.date),
                "to_date": (">=", self.date),
            },
        )
        if not valid_membership:
            frappe.throw(_("The member does not have a valid membership"))
    
    def validate_maximum_limit(self):
        # check if the member has reached the maximum limit of books they can issue
        max_books = frappe.db.get_single_value("Library Settings", "max_books")
        issued_books = frappe.db.count("Library Transaction", {"library_member": self.library_member, "type": "Issue", "docstatus": Docstatus.submitted()})

        if issued_books >= max_books:
           frappe.throw(_("The member has reached the maximum limit of books they can issue"))