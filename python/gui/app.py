import sys
import tkinter as tk
from tkinter import messagebox
from gui.theme import C, FONT_BODY, FONT_SMALL, sep
from gui.login_window import LoginWindow
from gui.base_page import BasePage
from gui.pages.dashboard import DashboardPage
from gui.pages.incomes import IncomesPage
from gui.pages.expenses import ExpensesPage
from gui.pages.report import ReportsPage
from gui.pages.account import AccountPage
from models.user import get_user_by_id

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("Personal Finance Manager")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(bg = C["bg_app"])
        self.current_user_id = None
        self.current_page = None
        self._pages = {}
        self._nav_btns = {}
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # bootstrap
    def start(self):
        LoginWindow(self, self._on_login)
        self.mainloop()

    def _on_login(self, user_id):
        self.current_user_id = user_id
        user = get_user_by_id(user_id)
        self._build_shell(user)
        self.deiconify()
        self._navigate("Dashboard")

    # shell (sidebar + content area)
    def _build_shell(self, user):
        # sidebar
        self.sidebar = tk.Frame(self, bg = C["bg_sidebar"], width = 210)
        self.sidebar.pack(side = "left", fill = "y")
        self.sidebar.pack_propagate(False)

        # logo
        logo_frame = tk.Frame(self.sidebar, bg = C["bg_sidebar"], pady = 24, padx = 20)
        logo_frame.pack(fill = "x")
        tk.Label(logo_frame, text = "💸 Finance", bg = C["bg_sidebar"],
                 fg = C["text_pri"], font = ("Segoe UI", 15, "bold")).pack(anchor = "w")
        tk.Label(logo_frame, text = "Personal Manager", bg = C["bg_sidebar"],
                 fg = C["text_muted"], font = FONT_SMALL).pack(anchor = "w")
            
        sep(self.sidebar, bg = C["border"]).pack(fill = "x", pady = 16)

        # User badge
        ub = tk.Frame(self.sidebar, bg = C["bg_sidebar"], padx = 14, pady = 14)
        ub.pack(fill = "x")
        av = tk.Frame(ub, bg = C["accent"], width = 36, height = 36)
        av.pack_propagate(False)
        av.pack(side = "left")
        initials = "".join(w[0].upper() for w in user["UserName"].split()[:2])
        tk.Label(av, text = initials, bg = C["accent"], fg = "white",
                 font = ("Segoe UI", 12, "bold")).place(relx = .5, rely = .5, anchor = "center")
        info = tk.Frame(ub, bg = C["bg_sidebar"], padx = 10)
        info.pack(side = "left", fill = "x")
        tk.Label(info, text = user["UserName"], bg = C["bg_sidebar"],
                 fg = C["text_pri"], font = ("Segoe UI", 11, "bold")).pack(anchor = "w")
        tk.Label(info, text = f"ID #{user['UserID']}", bg = C["bg_sidebar"],
                 fg = C["text_muted"], font = FONT_SMALL).pack(anchor = "w")
            
        sep(self.sidebar, bg = C["border"]).pack(fill = "x", padx = 16)

        # Nav items
        nav_items = [
            ("Dashboard","📊"),
            ("Incomes", "😘"),
            ("Expenses", "🥲"),
            ("Reports", "📝"),
            ("Account", "😎"),
        ]
        nav_frame = tk.Frame(self.sidebar, bg = C["bg_sidebar"], pady = 8)
        nav_frame.pack(fill = "x")
        for name, icon in nav_items:
            self._build_nav_btn(nav_frame, name, icon)
 
        sep(self.sidebar, bg = C["border"]).pack(fill = "x", padx = 16, side = "bottom", pady = 12)
        logout_frame = tk.Frame(self.sidebar, bg = C["bg_sidebar"], padx = 14, pady = 4)
        logout_frame.pack(side = "bottom", fill = "x")
        tk.Button(logout_frame, text = "👋 Log out",
                  bg = C["bg_sidebar"], fg = C["text_muted"], font = FONT_SMALL,
                  relief = "flat", bd = 0, cursor = "hand2", anchor = "w",
                  activebackground = C["bg_sidebar"], activeforeground = C["danger"],
                  command = self._logout).pack(fill = "x", ipady = 6)

        # content
        self.content = tk.Frame(self, bg = C["bg_app"])
        self.content.pack(side = "left", fill = "both", expand = True)

        # Build all pages
        self._pages = {
            "Dashboard": DashboardPage(self.content, self),
            "Incomes": IncomesPage(self.content, self),
            "Expenses": ExpensesPage(self.content, self),
            "Reports": ReportsPage(self.content, self),
            "Account": AccountPage(self.content, self),
        }
        for page in self._pages.values():
            page.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

    def _build_nav_btn(self, parent, name, icon):
        f = tk.Frame(parent, bg = C["bg_sidebar"], cursor = "hand2")
        f.pack(fill = "x", padx=10, pady = 1)
 
        icon_lbl = tk.Label(f, text = icon, bg = C["bg_sidebar"],
                            fg = C["text_muted"], font = ("Segoe UI", 13), width = 2)
        icon_lbl.pack(side = "left", padx = (8, 4), pady = 8)
        text_lbl = tk.Label(f, text = name, bg = C["bg_sidebar"],
                            fg = C["text_sec"], font = FONT_BODY)
        text_lbl.pack(side = "left", pady = 8)

        def on_enter(e):
            if self.current_page != name:
                f.config(bg = C["bg_hover"])
                icon_lbl.config(bg = C["bg_hover"])
                text_lbl.config(bg = C["bg_hover"])
        def on_leave(e):
            if self.current_page != name:
                f.config(bg = C["bg_sidebar"])
                icon_lbl.config(bg = C["bg_sidebar"])
                text_lbl.config(bg = C["bg_sidebar"])
        def on_click(e): self._navigate(name)

        for w in (f, icon_lbl, text_lbl):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)
        
        self._nav_btns[name] = (f, icon_lbl, text_lbl)

    def _navigate(self, name):
        # Reset old active
        if self.current_page and self.current_page in self._nav_btns:
            f, il, tl = self._nav_btns[self.current_page]
            f.config(bg = C["bg_sidebar"])
            il.config(bg = C["bg_sidebar"], fg = C["text_muted"])
            tl.config(bg = C["bg_sidebar"], fg = C["text_sec"])
 
        self.current_page = name
        f, il, tl = self._nav_btns[name]
        f.config(bg = C["bg_active"])
        il.config(bg = C["bg_active"], fg = C["accent_light"])
        tl.config(bg = C["bg_active"], fg = C["text_pri"], font = ("Segoe UI", 11, "bold"))

        page = self._pages[name]
        page.lift()
        page.refresh()

    def _logout(self):
        if messagebox.askyesno("Log out", "Return in login screen?"):
            self.destroy()
            # Restart
            app = FinanceApp()
            app.start()

    def on_closing(self):
        self.destroy()
        sys.exit(0)