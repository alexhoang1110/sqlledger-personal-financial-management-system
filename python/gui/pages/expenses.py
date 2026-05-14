import tkinter as tk
from tkinter import ttk
from datetime import date
from tkinter import messagebox
from gui.theme import (C, FONT_BODY, FONT_HEAD, FONT_SMALL, card, entry_field, btn, build_treeview)
from gui.base_page import BasePage
from models.expense import (add_expense, get_expenses_by_user, get_categories, delete_expense)

class ExpensesPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

    def refresh(self):
        for w in self.winfo_children(): w.destroy()
        self.page_header("Expenses", "Manage your spending")
        body = self.scrollable_body()

        two = tk.Frame(body, bg = C["bg_app"])
        two.pack(fill = "both", expand = True)
        two.columnconfigure(0, weight = 2)
        two.columnconfigure(1, weight = 3)

        # Add expense form
        form = card(two, padx = 20, pady = 18)
        form.grid(row = 0, column = 0, sticky = "nsew", padx = (0, 14))

        tk.Label(form, text = "Add Expense", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 14))
        
        # Category dropdown
        tk.Label(form, text = "Category", bg = C["bg_card"],
                 fg = C["text_sec"], font = FONT_SMALL).pack(anchor = "w", pady = (0, 2))
        cats = get_categories()
        cat_map = {c["CategoryName"]: c["CategoryID"] for c in cats}
 
        style = ttk.Style()
        style.configure("Dark.TCombobox",
                        fieldbackground = C["bg_input"],
                        background = C["bg_input"],
                        foreground = C["text_pri"],
                        arrowcolor = C["text_sec"],
                        borderwidth = 0)
        cat_var = tk.StringVar()
        combo = ttk.Combobox(form, textvariable = cat_var,
                             values = list(cat_map.keys()),
                             state = "readonly", style = "Dark.TCombobox",
                             font = FONT_BODY)
        combo.pack(fill = "x", ipady = 5)
        if cats: combo.current(0)

        fields = {}
        for lbl, ph in [("Amount ($)", "e.g. 150"),
                        ("Date", str(date.today())),
                        ("Description", "e.g. Dinner with friends")]:
            tk.Label(form, text = lbl, bg = C["bg_card"],
                     fg = C["text_sec"], font = FONT_SMALL).pack(anchor = "w", pady = (8, 2))
            e = entry_field(form, ph)
            e.pack(fill = "x", ipady = 7)
            fields[lbl] = e
        
        msg_var = tk.StringVar()
        msg_lbl = tk.Label(form, textvariable =msg_var, bg=C["bg_card"], fg=C["success"], font=FONT_SMALL)
        msg_lbl.pack(anchor="w", pady=(8, 0))

        def submit():
            try:
                cat_id = cat_map[cat_var.get()]
                amount = float(fields["Amount ($)"].get().replace(",", ""))
                d = fields["Date"].get().strip()
                desc = fields["Description"].get().strip()
                if desc in {"e.g. Dinner with friends", ""}:
                    desc = "Expense"
                result = add_expense(self.get_uid(), cat_id, amount, d, desc)
                if result and "RemainingBalance" in result[0]:
                    bal = float(result[0]["RemainingBalance"])
                    msg_var.set(f"Added! Balance: {bal:,.2f} $")
                else:
                    msg_var.set("Expense added successfully!")
                msg_lbl.config(fg = C["success"])
                self.refresh()
                self.app._pages["Dashboard"].refresh()
            except Exception as ex:
                msg_var.set(f"{ex}")
                msg_lbl.config(fg = C["danger"])

        btn(form, "Add Expense", command = submit, style = "danger").pack(fill = "x", pady = (14, 0), ipady = 3)

        # Expense history
        right = card(two, padx = 16, pady = 14)
        right.grid(row = 0, column = 1, sticky = "nsew")

        tk.Label(right, text = "Expense History", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 10))
        
        cols = ("ID", "Category", "Amount ($)", "Date", "Description")
        widths = [0, 110, 110, 90, 180]
        tf, tree = build_treeview(right, cols, widths, height=14)
        tf.pack(fill = "both", expand = True)

        tree.column("ID", width=0, minwidth=0, stretch=False)
        tree.heading("ID", text="")

        for r in get_expenses_by_user(self.get_uid()):
            tree.insert("", tk.END, values = (r["ExpenseID"], r["CategoryName"], f"{float(r['Amount']):,.2f}", str(r["ExpenseDate"]), r["Description"]))
            
        def delete_selected():
            selected_item = tree.focus()

            if not selected_item:
                messagebox.showwarning("No selection", "Please select an expense to delete.")
                return
            
            item_values = tree.item(selected_item, "values")
            expense_id = item_values[0]
            amount_str = item_values[2]
            desc_str = item_values[4]

            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this expense entry of ${amount_str} - {desc_str}?")
             
            if confirm:
                try:
                    delete_expense(expense_id)
                    messagebox.showinfo("Deleted", "Expense entry deleted successfully.")
                    self.refresh()
                    self.app._pages["Dashboard"].refresh()
                except Exception as ex:
                    messagebox.showerror("Error", f"An error occurred while deleting the expense: {ex}")
        
        btn(right, "Delete Selected", command=delete_selected, style="danger").pack(anchor="e", pady=(10, 0))