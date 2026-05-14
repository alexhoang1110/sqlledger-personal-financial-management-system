import tkinter as tk
from tkinter import messagebox
from datetime import date
from gui.theme import (C, FONT_HEAD, FONT_SMALL, card, entry_field, btn, build_treeview)
from gui.base_page import BasePage
from models.income import add_income, get_income_by_user, delete_income

class IncomesPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
 
    def refresh(self):
        for w in self.winfo_children(): w.destroy()
        self.page_header("Incomes", "Track your earnings")
        body = self.scrollable_body()

        two = tk.Frame(body, bg = C["bg_app"])
        two.pack(fill = "both", expand = True)
        two.columnconfigure(0, weight = 2)
        two.columnconfigure(1, weight = 3)

        # Add income form
        form = card(two, padx = 20, pady = 18)
        form.grid(row = 0, column = 0, sticky = "nsew", padx = (0, 14))

        tk.Label(form, text = "Add Income", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 14))
        
        fields = {}
        for lbl, ph in [("Amount ($)", "e.g. 500"),
                        ("Date", str(date.today())),
                        ("Description", "e.g. Monthly salary")]:
            tk.Label(form, text = lbl, bg = C["bg_card"],
                     fg = C["text_sec"], font = FONT_SMALL).pack(anchor = "w", pady = (6, 2))
            e = entry_field(form, ph)
            e.pack(fill = "x", ipady = 7)
            fields[lbl] = e

        msg_var = tk.StringVar()
        msg_lbl = tk.Label(form, textvariable = msg_var, bg = C["bg_card"],
                           fg = C["success"], font = FONT_SMALL)
        msg_lbl.pack(anchor = "w", pady = (8, 0))

        def submit():
            try:
                amount = float(fields["Amount ($)"].get().replace(",", ""))
                d = fields["Date"].get().strip()
                desc = fields["Description"].get().strip()
                if desc in {"e.g. Monthly salary", ""}:
                    desc = "Income"
                add_income(self.get_uid(), amount, d, desc)
                msg_var.set("Income added successfully!")
                msg_lbl.config(fg = C["success"])
                self.refresh()
                self.app._pages["Dashboard"].refresh()
            except Exception as ex:
                msg_var.set(f"{ex}")
                msg_lbl.config(fg = C["danger"])
        
        btn(form, "Add Income", command = submit, style = "success").pack(fill = "x", pady = (14, 0), ipady = 3)

        # Income history table
        right = card(two, padx = 16, pady = 14)
        right.grid(row = 0, column = 1, sticky = "nsew")
 
        tk.Label(right, text = "Income History", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 10))
 
        cols   = ("ID", "Date", "Amount ($)", "Description")
        widths = [0, 100, 130, 220] # ID có width=0
        tf, tree = build_treeview(right, cols, widths, height = 14)
        
        # Ẩn cột ID đi để không làm xấu giao diện
        tree.column("ID", width=0, stretch=tk.NO)
        tree.heading("ID", text="")
        
        tf.pack(fill = "both", expand = True)
 
        for r in get_income_by_user(self.get_uid()):
            # THÊM r["IncomeID"] vào vị trí đầu tiên của values
            tree.insert("", tk.END, values = (r["IncomeID"], str(r["IncomeDate"]), f"{float(r['Amount']):,.2f}", r["Description"]))
            
        def delete_selected():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("No selection", "Please select an income entry to delete.")
                return
            
            item_values = tree.item(selected_item, "values")
            income_id = item_values[0]   # Bây giờ [0] đã trỏ đúng vào IncomeID
            amount_str = item_values[2]  # Và [2] đã trỏ đúng vào số tiền Amount

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this income entry of ${amount_str}?")
            if confirm:
                try:
                    delete_income(income_id)
                    messagebox.showinfo("Deleted", "Income entry deleted successfully.")
                    self.refresh()
                    self.app._pages["Dashboard"].refresh()
                except Exception as ex:
                    messagebox.showerror("Error", f"An error occurred while deleting: {ex}")
        
        btn(right, "Delete Selected", command=delete_selected, style="danger").pack(anchor="e", pady=(10, 0))