import tkinter as tk
from gui.theme import (C, FONT_BODY, FONT_HEAD, FONT_SMALL, card, build_treeview)
from gui.base_page import BasePage
from models.account import get_monthly_summary, get_category_spending

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

class ReportsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)

    def refresh(self):
        for w in self.winfo_children(): w.destroy()
        self.page_header("Reports & Analytics", "Visual insights into your finances")
 
        if not HAS_MATPLOTLIB:
            tk.Label(self, text = "Please install matplotlib: \npip install matplotlib",
                     bg=C["bg_app"], fg=C["text_muted"], font = FONT_BODY).pack(expand = True)
            return

        body = self.scrollable_body()
        uid  = self.get_uid()

        # Monthly summary table
        sec1 = card(body, padx = 16, pady = 14)
        sec1.pack(fill = "x", pady = (0, 16))
        tk.Label(sec1, text = "Monthly Financial Summary", bg = C["bg_card"],
                 fg=C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 10))
 
        cols = ("Year", "Month", "Total Income", "Total Expense", "Net Savings", "Status")
        widths = [60, 60, 140, 140, 140, 90]
        tf, tree = build_treeview(sec1, cols, widths, height = 5)
        tf.pack(fill = "x")

        summary = get_monthly_summary(uid)
        for r in summary:
            net = float(r["TotalIncome"]) - float(r["TotalExpense"])
            status = "SURPLUS" if net > 0 else ("DEFICIT" if net < 0 else "BALANCED")
            tree.insert("", tk.END, values = (
                r["ReportYear"], r["ReportMonth"],
                f"{float(r['TotalIncome']):,.0f}",
                f"{float(r['TotalExpense']):,.0f}",
                f"{net:,.0f}", status))
            
        # Charts
        charts_row = tk.Frame(body, bg = C["bg_app"])
        charts_row.pack(fill = "both", expand = True)
        charts_row.columnconfigure(0, weight = 1)
        charts_row.columnconfigure(1, weight = 1)

        # Bar chart
        left = card(charts_row, padx = 14, pady = 14)
        left.grid(row = 0, column = 0, sticky = "nsew", padx = (0, 10))
        tk.Label(left, text = "Income vs Expense by Month", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 8))
        if summary:
            fig1, ax1 = plt.subplots(figsize = (5, 3.5), facecolor = C["bg_card"])
            ax1.set_facecolor(C["bg_card"])
            lbls = [f"{r['ReportMonth']}/{str(r['ReportYear'])[2:]}" for r in summary]
            inc_v = [float(r["TotalIncome"]) for r in summary]
            exp_v = [float(r["TotalExpense"]) for r in summary]
            x = range(len(lbls))
            ax1.bar([i-.2 for i in x], inc_v, width = .35, color = "#22c55e", alpha = .85, label = "Income")
            ax1.bar([i+.2 for i in x], exp_v, width = .35, color = "#ef4444", alpha = .85, label = "Expense")
            ax1.set_xticks(list(x)); ax1.set_xticklabels(lbls, color = C["text_muted"], fontsize = 8)
            ax1.tick_params(colors = C["text_muted"], labelsize = 7)
            ax1.spines[:].set_visible(False)
            ax1.legend(fontsize = 7, facecolor = C["bg_card"], labelcolor = C["text_sec"], framealpha = .8)
            ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v / 1e6:.1f}M" if v >= 1e6 else f"{v / 1e3:.0f}K"))
            fig1.tight_layout(pad = 1.2)
            c1 = FigureCanvasTkAgg(fig1, master = left)
            c1.draw(); c1.get_tk_widget().pack(fill = "both", expand = True)

        # Pie chart
        right = card(charts_row, padx = 14, pady = 14)
        right.grid(row = 0, column = 1, sticky = "nsew")
        tk.Label(right, text = "Spending by Category", bg = C["bg_card"],
                 fg = C["text_pri"], font = FONT_HEAD).pack(anchor = "w", pady = (0, 8))
        
        cat_data = get_category_spending(uid)
        if cat_data:
            fig2, ax2 = plt.subplots(figsize = (5, 3.5), facecolor = C["bg_card"])
            ax2.set_facecolor(C["bg_card"])
            cat_lbls = [r["CategoryName"] for r in cat_data]
            cat_vals = [float(r["TotalAmount"]) for r in cat_data]
            wedge_colors = ["#3b82f6","#22c55e","#ef4444","#f59e0b",
                            "#a855f7","#06b6d4","#f97316","#ec4899"]
            wedges, _, autotexts = ax2.pie(
                cat_vals, labels = cat_lbls, autopct = "%1.0f%%",
                colors = wedge_colors[:len(cat_vals)], startangle = 140,
                textprops = {"color": C["text_muted"], "fontsize": 8})
            for at in autotexts: at.set_color(C["text_pri"]); at.set_fontsize(7)
            fig2.tight_layout(pad = 0.5)
            c2 = FigureCanvasTkAgg(fig2, master = right)
            c2.draw(); c2.get_tk_widget().pack(fill = "both", expand = True)
        else:
            tk.Label(right, text = "No expense data yet",
                     bg = C["bg_card"], fg = C["text_muted"],
                     font = FONT_SMALL).pack(expand = True)