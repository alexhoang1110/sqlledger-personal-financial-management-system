import tkinter as tk
from tkinter import ttk
from datetime import date
from gui.theme import (C, FONT_HEAD, FONT_SMALL, card, stat_card, sep, build_treeview)
from gui.base_page import BasePage
from models.income import get_income_by_user, get_monthly_income
from models.expense import get_expenses_by_user, get_monthly_expense, get_budget_status
from models.account import get_total_balance, get_monthly_summary

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

    def refresh(self):
        for w in self.winfo_children(): w.destroy()
        uid = self.get_uid()
        today = date.today()
        m, y = today.month, today.year

        self.page_header("Dashboard", f"Overview for {today.strftime('%B %Y')}")

        body = self.scrollable_body()

        # Stat cards
        inc_raw = get_monthly_income(uid, m, y)
        exp_raw = get_monthly_expense(uid, m, y)
        inc_val = float(inc_raw[0]) if isinstance(inc_raw, tuple) else float(inc_raw or 0)
        exp_val = float(exp_raw[0]) if isinstance(exp_raw, tuple) else float(exp_raw or 0)
        net_val = float(inc_val) - float(exp_val)
        bal_val = get_total_balance(uid) or 0
        status  = get_budget_status(uid, m, y)

        stat_row = tk.Frame(body, bg = C['bg_app'])
        stat_row.pack(fill = "x", pady = (0, 18))

        stats = [
            ("Monthly Income", f"{float(inc_val):,.0f}", "$", C["success"]),
            ("Monthly Expense", f"{float(exp_val):,.0f}", "$", C["danger"]),
            ("Net Savings", f"{net_val:,.0f}", "$",
            C["success"] if net_val >= 0 else C["danger"]),
            ("Total Balance",   f"{float(bal_val):,.0f}", "$", C["accent_light"]),]
        for i, (title, value, unit, colour) in enumerate(stats):
            sc = stat_card(stat_row, title, value, unit, colour)
            sc.grid(row = 0, column = i, padx = (0, 12) if i < 3 else 0, sticky = "nsew")
        for i in range(4):
            stat_row.grid_columnconfigure(i, weight = 1)

        # Budget status
        badge_colour = C["success"] if status == "SURPLUS" else (C["danger"]  if status == "DEFICIT" else C["warning"])
        badge = tk.Frame(body, bg = badge_colour, padx = 12, pady = 4)
        badge.pack(anchor = "w", pady = (0, 18))
        tk.Label(badge, text = f"Budget Status: {status}",
                 bg = badge_colour, fg = "white", font = ("Segoe UI", 10, "bold")).pack()
        
        # Two-column: transaction + chart
        two_col = tk.Frame(body, bg = C["bg_app"])
        two_col.pack(fill = "both", expand = True)
        two_col.columnconfigure(0, weight = 3)
        two_col.columnconfigure(1, weight = 2)

        # Recent transactions
        left = card(two_col, padx = 16, pady = 14)
        left.grid(row = 0, column = 0, sticky = "nsew", padx = (0, 12))

        tk.Label(left, text = "Recent Transactions", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 10))
        
        cols = ("Date", "Description", "Amount", "Type")
        widths = [90, 200, 110, 80]
        tf, tree = build_treeview(left, cols, widths, height = 8)
        tf.pack(fill = "both", expand = True)

        expenses = get_expenses_by_user(uid)[:5]
        incomes = get_income_by_user(uid)[:5]
        rows_all = []
        for r in incomes:
            rows_all.append((str(r["IncomeDate"]), r["Description"],
                             f"+{float(r['Amount']):,.0f}", "Income"))
        for r in expenses:
            rows_all.append((str(r["ExpenseDate"]), r["Description"],
                             f"-{float(r['Amount']):,.0f}", "Expense"))
        rows_all.sort(key = lambda x: x[0], reverse = True)
        for row in rows_all[:8]:
            tree.insert("", tk.END, values = row)

        # Monthly bar chart
        right = card(two_col, padx = 16, pady = 14)
        right.grid(row = 0, column = 1, sticky = "nsew")
        tk.Label(right, text = "Monthly Overview", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 10))
        
        summary = get_monthly_summary(uid)
        if HAS_MATPLOTLIB and summary:
            fig, ax = plt.subplots(figsize = (4, 3.2), facecolor = C["bg_card"])
            ax.set_facecolor(C["bg_card"])
            labels = [f"{r['ReportMonth']}/{str(r['ReportYear'])[2:]}" for r in summary[-4:]]
            inc_v = [float(r["TotalIncome"]) for r in summary[-4:]]
            exp_v = [float(r["TotalExpense"]) for r in summary[-4:]]
            x = range(len(labels))
            ax.bar([i-.2 for i in x], inc_v, width = .35, color="#22c55e", alpha = .85, label = "Income")
            ax.bar([i+.2 for i in x], exp_v, width = .35, color="#ef4444", alpha = .85, label = "Expense")
            ax.set_xticks(list(x)); ax.set_xticklabels(labels, color = C["text_muted"], fontsize = 8)
            ax.tick_params(axis = "y", colors = C["text_muted"], labelsize = 7)
            ax.spines[:].set_visible(False)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v / 1e3:.0f}K"))
            legend = ax.legend(fontsize = 7, facecolor = C["bg_card"], labelcolor = C["text_sec"], framealpha = .8)
            fig.tight_layout(pad = 1)
            canvas_widget = FigureCanvasTkAgg(fig, master = right)
            canvas_widget.draw()
            canvas_widget.get_tk_widget().pack(fill = "both", expand = True)
        else:
            tk.Label(right, text = "Install matplotlib \nto see charts",
                     bg = C["bg_card"], fg = C["text_muted"], font = FONT_SMALL).pack(expand = True)