import tkinter as tk
from gui.theme import (C, FONT_HEAD, FONT_SMALL, card, entry_field, btn, build_treeview)
from gui.base_page import BasePage
from models.user import create_user

class UsersPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
 
    def refresh(self):
        for w in self.winfo_children(): w.destroy()
        self.page_header("User Management", "All registered profiles")
        body = self.scrollable_body()
 
        # Create user form
        form = card(body, padx = 20, pady = 18)
        form.pack(fill = "x", pady = (0, 16))
        tk.Label(form, text="Create New User", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 12))
 
        row = tk.Frame(form, bg = C["bg_card"])
        row.pack(fill = "x")
        fields = {}
        for lbl, ph in [("Name", "Full name"),
                        ("Email", "Email address"),
                        ("Phone", "Phone number")]:
            col = tk.Frame(row, bg = C["bg_card"])
            col.pack(side = "left", fill = "x", expand = True, padx = (0, 10))
            tk.Label(col, text=lbl, bg = C["bg_card"], fg = C["text_sec"],
                     font = FONT_SMALL).pack(anchor = "w", pady = (0, 3))
            e = entry_field(col, ph, width = 20)
            e.pack(fill = "x", ipady = 7)
            fields[lbl] = e
 
        msg_var = tk.StringVar()
        tk.Label(form, textvariable=msg_var, bg = C["bg_card"],
                 fg = C["success"], font = FONT_SMALL).pack(anchor = "w", pady = (8, 0))
 
        def create():
            try:
                name = fields["Name"].get().strip()
                email = fields["Email"].get().strip()
                phone = fields["Phone"].get().strip()
                if name in {"Full name", ""}:
                    raise ValueError("Name is required")
                if email in {"Email address", ""}:
                    raise ValueError("Email is required")
                uid = create_user(name, email, phone if phone != "Phone number" else "")
                msg_var.set(f"User created with ID #{uid}")
                self.refresh()
            except Exception as ex:
                msg_var.set(f"{ex}")
 
        btn(form, "Create User", command = create, style = "primary").pack(
            anchor = "w", pady = (10, 0), ipady = 3)
 
        # Users table
        tbl = card(body, padx = 16, pady = 14)
        tbl.pack(fill = "both", expand = True)
        tk.Label(tbl, text = "All Users", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 10))
 
        cols = ("ID", "Name", "Email", "Phone", "Created")
        widths = [40, 160, 200, 120, 150]
        tf, tree = build_treeview(tbl, cols, widths, height = 10)
        tf.pack(fill = "both", expand = True)
 
        from database import fetch_all
        users = fetch_all("SELECT * FROM Users ORDER BY UserID")
        for u in users:
            tree.insert("", tk.END, values = (
                u["UserID"], u["UserName"], u["Email"],
                u.get("PhoneNumber", "—"),
                str(u.get("CreatedAt", "—"))))