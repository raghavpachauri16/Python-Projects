"""
Contact Book (GUI)
------------------
A simple, user-friendly contact management app built with Tkinter.

Features:
    - Add Contact:     Save name, phone, email, and address
    - View Contacts:   List of all contacts (name + phone)
    - Search Contact:  Find contacts by name or phone number
    - Update Contact:  Edit an existing contact's details
    - Delete Contact:  Remove a contact

Data is stored persistently in 'contacts.json' in the same folder
as this script, so your contacts are saved between runs.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.json")

# Validation patterns
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9\s\-]{6,14}[0-9]$")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


# ---------------- Data Layer ----------------
def load_contacts():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_contacts(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)


contacts = load_contacts()
selected_index = None  # Index (in `contacts`) of the currently selected contact


# ---------------- Helper Functions ----------------
def refresh_list(filtered=None):
    """Repopulate the Treeview with contacts (or a filtered subset)."""
    tree.delete(*tree.get_children())
    data = filtered if filtered is not None else contacts
    for i, c in enumerate(data):
        # Store the true index into `contacts` as the item's iid when filtering
        true_index = contacts.index(c) if filtered is not None else i
        tree.insert("", "end", iid=str(true_index), values=(c["name"], c["phone"]))


def clear_form():
    global selected_index
    selected_index = None
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    address_var.set("")
    tree.selection_remove(tree.selection())


def on_select(event):
    """When a contact is clicked in the list, load its details into the form."""
    global selected_index
    sel = tree.selection()
    if not sel:
        return
    selected_index = int(sel[0])
    c = contacts[selected_index]
    name_var.set(c["name"])
    phone_var.set(c["phone"])
    email_var.set(c["email"])
    address_var.set(c["address"])


def validate_form():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if not name:
        messagebox.showerror("Missing Info", "Name is required.")
        return None
    if not phone:
        messagebox.showerror("Missing Info", "Phone number is required.")
        return None
    if not PHONE_PATTERN.match(phone):
        messagebox.showerror(
            "Invalid Phone Number",
            "Phone number looks invalid.\nUse digits only (7-15 of them), "
            "optionally with spaces, dashes, or a leading +.\n"
            "Example: +1 555-123-4567",
        )
        return None
    if email and not EMAIL_PATTERN.match(email):
        messagebox.showerror(
            "Invalid Email",
            "Email address looks invalid.\nExample: name@example.com",
        )
        return None

    return {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address_var.get().strip(),
    }


# ---------------- Core Actions ----------------
def add_contact():
    data = validate_form()
    if not data:
        return
    contacts.append(data)
    save_contacts(contacts)
    refresh_list()
    clear_form()
    show_toast(f"Contact '{data['name']}' added.")


def update_contact():
    if selected_index is None:
        messagebox.showwarning("No Selection", "Select a contact from the list to update.")
        return
    data = validate_form()
    if not data:
        return
    contacts[selected_index] = data
    save_contacts(contacts)
    refresh_list()
    clear_form()
    show_toast(f"Contact '{data['name']}' updated.")


def delete_contact():
    if selected_index is None:
        messagebox.showwarning("No Selection", "Select a contact from the list to delete.")
        return
    name = contacts[selected_index]["name"]
    if messagebox.askyesno("Confirm Delete", f"Delete contact '{name}'?"):
        del contacts[selected_index]
        save_contacts(contacts)
        refresh_list()
        clear_form()
        show_toast(f"Contact '{name}' deleted.", kind="info")


def search_contact():
    query = search_var.get().strip().lower()
    if not query:
        refresh_list()
        return
    results = [
        c for c in contacts
        if query in c["name"].lower() or query in c["phone"].lower()
    ]
    if not results:
        show_toast("No matching contacts found.", kind="info")
    else:
        show_toast(f"Found {len(results)} matching contact(s).", kind="info")
    refresh_list(filtered=results)


def reset_search():
    search_var.set("")
    refresh_list()


# ---------------- Toast / Snackbar ----------------
_toast_job = None  # tracks the pending auto-dismiss callback


def show_toast(message, kind="success"):
    """Show a small, non-blocking confirmation banner that auto-dismisses."""
    global _toast_job

    colors = {
        "success": ("#4CAF50", "white"),
        "info": ("#333333", "white"),
    }
    bg, fg = colors.get(kind, colors["success"])

    toast_label.config(text=message, bg=bg, fg=fg)
    toast_label.place(relx=0.5, rely=0.965, anchor="s")

    # Cancel any previous pending dismissal so toasts don't cut each other off
    if _toast_job is not None:
        root.after_cancel(_toast_job)
    _toast_job = root.after(2200, toast_label.place_forget)


# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Contact Book")
root.geometry("800x500")
root.resizable(False, False)

name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
address_var = tk.StringVar()
search_var = tk.StringVar()

# ---- Title ----
tk.Label(root, text="Contact Book", font=("Arial", 18, "bold")).pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=15)

# ---- Left: Contact Form ----
form_frame = tk.LabelFrame(main_frame, text="Contact Details", padx=10, pady=10)
form_frame.grid(row=0, column=0, sticky="n", padx=(0, 15))

fields = [
    ("Name:", name_var),
    ("Phone:", phone_var),
    ("Email:", email_var),
    ("Address:", address_var),
]
for i, (label, var) in enumerate(fields):
    tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=6)
    tk.Entry(form_frame, textvariable=var, width=28).grid(row=i, column=1, padx=5, pady=6)

btn_frame = tk.Frame(form_frame)
btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="Add", width=9, bg="#4CAF50", fg="white", command=add_contact).grid(row=0, column=0, padx=3)
tk.Button(btn_frame, text="Update", width=9, bg="#2196F3", fg="white", command=update_contact).grid(row=0, column=1, padx=3)
tk.Button(btn_frame, text="Delete", width=9, bg="#f44336", fg="white", command=delete_contact).grid(row=0, column=2, padx=3)
tk.Button(form_frame, text="Clear Form", width=30, command=clear_form).grid(row=len(fields) + 1, column=0, columnspan=2, pady=(0, 5))

# ---- Right: Contact List + Search ----
list_frame = tk.Frame(main_frame)
list_frame.grid(row=0, column=1, sticky="n")

search_bar = tk.Frame(list_frame)
search_bar.pack(fill="x", pady=(0, 8))
tk.Entry(search_bar, textvariable=search_var, width=28).pack(side="left", padx=(0, 5))
tk.Button(search_bar, text="Search", command=search_contact).pack(side="left", padx=2)
tk.Button(search_bar, text="Reset", command=reset_search).pack(side="left", padx=2)

tree = ttk.Treeview(list_frame, columns=("name", "phone"), show="headings", height=15)
tree.heading("name", text="Name")
tree.heading("phone", text="Phone")
tree.column("name", width=180)
tree.column("phone", width=140)
tree.pack()
tree.bind("<<TreeviewSelect>>", on_select)

tk.Label(root, text="Select a contact from the list to update or delete it.", font=("Arial", 9), fg="gray").pack(pady=8)

# Toast/snackbar widget (hidden until show_toast() places it)
toast_label = tk.Label(root, text="", font=("Arial", 10), padx=14, pady=6)

refresh_list()
root.mainloop()
