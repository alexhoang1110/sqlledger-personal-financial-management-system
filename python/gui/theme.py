import tkinter as tk
from tkinter import ttk

# COLOUR PALETTE
C = {
    "bg_app":      "#0f1117",
    "bg_sidebar":  "#161b27",
    "bg_card":     "#1c2333",
    "bg_input":    "#242a3a",
    "bg_hover":    "#1e2a40",
    "bg_active":   "#1a3a5c",
    "accent":      "#3b82f6",
    "accent_dark": "#1d4ed8",
    "accent_light":"#93c5fd",
    "success":     "#22c55e",
    "danger":      "#ef4444",
    "warning":     "#f59e0b",
    "text_pri":    "#f1f5f9",
    "text_sec":    "#94a3b8",
    "text_muted":  "#475569",
    "border":      "#1e2a3a",
    "border_light":"#2d3748",
}

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEAD = ("Segoe UI", 13, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 11)

# HELPER WIDGETS
def card(parent, **kw):
    kw.setdefault("bg", C["bg_card"])
    kw.setdefault("bd", 0)
    kw.setdefault("relief", "flat")
    f = tk.Frame(parent, **kw)
    return f

def label(parent, text = "", style = "body", **kw):
    colours = {"title": C["text_pri"], "head": C["text_pri"],
               "body": C["text_sec"], "muted": C["text_muted"],
               "accent": C["accent_light"], "success": C["success"],
               "danger": C["danger"]}
    fonts = {"title": FONT_TITLE, "head": FONT_HEAD,
             "body": FONT_BODY,   "muted": FONT_SMALL,
             "accent": FONT_BODY, "success": FONT_BODY, "danger": FONT_BODY}
    kw.setdefault("bg",   C["bg_card"])
    kw.setdefault("fg",   colours.get(style, C["text_sec"]))
    kw.setdefault("font", fonts.get(style, FONT_BODY))
    return tk.Label(parent, text=text, **kw)

def sep(parent, **kw):
    kw.setdefault("bg", C["border"])
    kw.setdefault("height", 1)
    return tk.Frame(parent, **kw)

def entry_field(parent, placeholder = "", width=28, show = ""):
    e = tk.Entry(parent, bg = C["bg_input"], fg = C["text_pri"],
                 insertbackground = C["accent"], relief = "flat",
                 font = FONT_BODY, bd = 0, highlightthickness = 1,
                 highlightbackground = C["border_light"],
                 highlightcolor = C["accent"], width = width, show = show)
    if placeholder:
        e.insert(0, placeholder)
        e.config(fg = C["text_muted"])
        def on_focus_in(ev):
            if e.get() == placeholder:
                e.delete(0, tk.END); e.config(fg = C["text_pri"])
        def on_focus_out(ev):
            if e.get() == "":
                e.insert(0, placeholder); e.config(fg=C["text_muted"])
        e.bind("<FocusIn>",  on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
    return e

def btn(parent, text, command = None, style = "primary", **kw):
    colours = {
        "primary": (C["accent"],      C["text_pri"],   C["accent_dark"]),
        "success": (C["success"],     C["text_pri"],   "#16a34a"),
        "danger":  (C["danger"],      C["text_pri"],   "#dc2626"),
        "ghost":   (C["bg_input"],    C["text_sec"],   C["bg_hover"]),
    }
    bg, fg, hov = colours.get(style, colours["primary"])
    b = tk.Button(parent, text = text, command = command,
                  bg = bg, fg = fg, font = FONT_BODY, relief = "flat", bd = 0,
                  cursor = "hand2", padx = 16, pady = 7, activebackground  = hov,
                  activeforeground = fg, **kw)
    return b

def stat_card(parent, title, value, unit = "$", colour = None):
    colour = colour or C["accent_light"]
    f = card(parent, padx = 16, pady = 14)
    tk.Label(f, text = title, bg = C["bg_card"], fg = C["text_muted"],
             font = FONT_SMALL).pack(anchor = "w")
    tk.Label(f, text = value, bg = C["bg_card"], fg = colour,
             font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(2, 0))
    tk.Label(f, text = unit, bg = C["bg_card"], fg = C["text_muted"],
             font = FONT_SMALL).pack(anchor = "w")
    return f

def build_treeview(parent, columns, col_widths = None, height = 10):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.Treeview",
                    background = C["bg_card"], foreground = C["text_sec"],
                    fieldbackground = C["bg_card"], borderwidth = 0,
                    rowheight = 28, font = FONT_BODY)
    style.configure("Dark.Treeview.Heading",
                    background = C["bg_input"], foreground = C["text_pri"],
                    borderwidth = 0, font = ("Segoe UI", 10, "bold"))
    style.map("Dark.Treeview", background = [("selected", C["bg_active"])],
              foreground =[("selected", C["text_pri"])])
    
    frame = tk.Frame(parent, bg = C["bg_card"])
    tree  = ttk.Treeview(frame, columns = columns, show = "headings",
                         height = height, style = "Dark.Treeview")
    vsb   = ttk.Scrollbar(frame, orient = "vertical", command = tree.yview)
    tree.configure(yscrollcommand = vsb.set)

    style.configure("Dark.Vertical.TScrollbar",
                    background = C["bg_input"], troughcolor = C["bg_card"],
                    arrowcolor = C["text_muted"])
    vsb.configure(style = "Dark.Vertical.TScrollbar")

    for i, col in enumerate(columns):
        tree.heading(col, text = col)
        w = (col_widths[i] if col_widths and i < len(col_widths) else 120)
        tree.column(col, width = w, minwidth=60, anchor = "w")
 
    tree.pack(side = "left", fill = "both", expand=True)
    vsb.pack(side = "right", fill = "y")
    return frame, tree