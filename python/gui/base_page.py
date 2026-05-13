import tkinter as tk
from gui.theme import C, FONT_HEAD, FONT_SMALL, sep

class BasePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg = C["bg_app"])
        self.app = app

    def refresh(self): pass

    def get_uid(self): return self.app.current_user_id

    def page_header(self, title, subtitle=""):
        hdr = tk.Frame(self, bg = C["bg_app"], pady = 20, padx = 28)
        hdr.pack(fill = "x")
        tk.Label(hdr, text = title, bg = C["bg_app"], fg = C["text_pri"], font = ("Segoe UI", 18, "bold")).pack(anchor = "w")
        if subtitle:
            tk.Label(hdr, text = subtitle, bg = C["bg_app"], fg = C["text_muted"], font = FONT_SMALL).pack(anchor = "w", pady = (2, 0))
        sep(self, bg = C["border"]).pack(fill = "x", padx = 28)
        return hdr
    
    def scrollable_body(self):
        outer = tk.Frame(self, bg = C["bg_app"])
        outer.pack(fill = "both", expand = True, padx = 28, pady = 16)
        canvas = tk.Canvas(outer, bg = C["bg_app"], highlightthickness = 0)
        vsb = tk.Scrollbar(outer, orient = "vertical", command = canvas.yview)
        canvas.configure(yscrollcommand = vsb.set)
        vsb.pack(side = "right", fill = "y")
        canvas.pack(side = "left", fill = "both", expand = True)
        inner = tk.Frame(canvas, bg = C["bg_app"])
        win = canvas.create_window((0, 0), window = inner, anchor = "nw")
        def on_cfg(e):
            canvas.configure(scrollregion = canvas.bbox("all"))
            canvas.itemconfig(win, width = canvas.winfo_width())
        inner.bind("<Configure>", on_cfg)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width = e.width))
        inner.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        return inner