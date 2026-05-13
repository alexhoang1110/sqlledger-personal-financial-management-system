import tkinter as tk
from gui.theme import (C, FONT_HEAD, FONT_SMALL, card, sep, build_treeview)
from gui.base_page import BasePage
from models.account import get_accounts_by_user, get_total_balance
from database import fetch_all

class AccountPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
 
    def refresh(self):
        for w in self.winfo_children(): w.destroy()
        uid = self.get_uid()
        self.page_header("Bank Accounts", "Your account balances")
        body = self.scrollable_body()
 
        accounts  = get_accounts_by_user(uid)
        total_bal = get_total_balance(uid)

        # Total balance
        tb = card(body, padx = 20, pady = 16)
        tb.pack(fill = "x", pady = (0, 16))
        tk.Label(tb, text="Total Balance Across All Accounts",
                 bg = C["bg_card"], fg = C["text_muted"],
                 font = FONT_SMALL).pack(anchor = "w")
        tk.Label(tb, text = f"{float(total_bal):,.0f} $",
                 bg = C["bg_card"], fg = C["accent_light"],
                 font = ("Segoe UI", 24, "bold")).pack(anchor = "w", pady = (4, 0))
        
        # Accounts cards grid
        grid = tk.Frame(body, bg = C["bg_app"])
        grid.pack(fill = "x")
        for i, acc in enumerate(accounts):
            ac = card(grid, padx = 18, pady = 16)
            ac.grid(row = i // 3, column = i % 3, padx = (0, 12) if i % 3 < 2 else 0,
                    pady = (0, 12), sticky = "nsew")
            grid.columnconfigure(i % 3, weight = 1)
 
            tk.Label(ac, text=acc["BankName"], bg = C["bg_card"],
                     fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w")
            tk.Label(ac, text = f"Account ID: #{acc['AccountID']}",
                     bg = C["bg_card"], fg = C["text_muted"],
                     font = FONT_SMALL).pack(anchor = "w", pady = (2, 8))
            sep(ac, bg = C["border_light"]).pack(fill = "x", pady = (0, 8))
            tk.Label(ac, text = f"{float(acc['Balance']):,.0f}",
                     bg = C["bg_card"], fg = C["success"],
                     font = ("Segoe UI", 18, "bold")).pack(anchor = "w")
            tk.Label(ac, text = "$", bg = C["bg_card"],
                     fg = C["text_muted"], font = FONT_SMALL).pack(anchor = "w")
        
        # Audit log
        log_frame = card(body, padx = 16, pady = 14)
        log_frame.pack(fill = "x", pady = (16, 0))
        tk.Label(log_frame, text = "Balance Audit Log", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 10))
        
        logs = fetch_all(
            """SELECT l.LogID, b.BankName, l.OldBalance, l.NewBalance, l.ChangeType, l.ChangedAt
               FROM BalanceAuditLog l
               JOIN BankAccounts b ON l.AccountID = b.AccountID
               WHERE b.UserID = %s
               ORDER BY l.ChangedAt DESC LIMIT 20""", (uid,))
        
        cols = ("ID", "Bank", "Old Balance", "New Balance", "Type", "Timestamp")
        widths = [40, 120, 120, 120, 80, 160]
        tf, tree = build_treeview(log_frame, cols, widths, height=8)
        tf.pack(fill = "both", expand = True)
        for r in logs:
            tree.insert("", tk.END, values = (
                r["LogID"], r["BankName"],
                f"{float(r['OldBalance']):,.0f}",
                f"{float(r['NewBalance']):,.0f}",
                r["ChangeType"], str(r["ChangedAt"])))