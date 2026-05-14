import tkinter as tk
from tkinter import messagebox
from gui.theme import C, FONT_SMALL, entry_field, btn, sep
from models.user import create_initial_account, get_user_by_id, login_user, create_user

#  LOGIN WINDOW
class LoginWindow(tk.Toplevel):
    def __init__(self, master, on_login):
        super().__init__(master)
        self.on_login  = on_login
        self.title("Personal Finance Manager - Login")
        self.geometry("1920x1080")
        self.resizable(True, True)
        self.configure(bg=C["bg_app"])
        self.grab_set()
        self._show_login()

    # LOGIN FORM
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _show_login(self):
        self._clear()

        hdr = tk.Frame(self, bg = C["bg_app"], pady = 36)
        hdr.pack(fill = "x")
        tk.Label(hdr, text = "💸", bg = C["bg_app"],
                 font = ("Segoe UI", 36)).pack()
        tk.Label(hdr, text = "Finance Manager", bg = C["bg_app"],
                 fg = C["text_pri"], font = ("Segoe UI", 18, "bold")).pack(pady = (6, 2))
        tk.Label(hdr, text = "Sign in to your account", bg = C["bg_app"],
                 fg=  C["text_muted"], font = FONT_SMALL).pack()
        
        body = tk.Frame(self, bg = C["bg_app"], padx = 40)
        body.pack(fill = "both", expand = True)

        tk.Label(body, text = "Email", bg = C["bg_app"],
                 fg = C["text_sec"], font = FONT_SMALL).pack(anchor = "w", pady = (16, 3))
        self.e_email = entry_field(body, "Enter your email")
        self.e_email.pack(fill = "x", ipady = 8)

        tk.Label(body, text = "Password", bg = C["bg_app"],
                 fg = C["text_sec"], font = FONT_SMALL).pack(anchor = "w", pady = (12, 3))
        self.e_pass = entry_field(body, "Enter your password", show = "•")
        self.e_pass.pack(fill = "x", ipady = 8)

        self.msg_var = tk.StringVar()
        tk.Label(body, textvariable = self.msg_var, bg = C["bg_app"],
                 fg = C["danger"], font = FONT_SMALL).pack(anchor = "w", pady = (8, 0))

        btn(body, "Login", command = self._do_login,
            style = "primary").pack(fill = "x", pady = (12, 0), ipady = 4)
        
        sep(body, bg = C["border_light"]).pack(fill = "x", pady = 20)

        foot = tk.Frame(body, bg = C["bg_app"])
        foot.pack(fill = "x", pady = (0, 30))
        tk.Label(foot, text = "Don't have an account?", bg = C["bg_app"],
                 fg = C["text_muted"], font = FONT_SMALL).pack(side = "left")
        tk.Label(foot, text = " Create one", bg = C["bg_app"],
                 fg = C["accent_light"], font = ("Segoe UI", 10, "bold"),
                 cursor = "hand2").pack(side = "left")
        foot.winfo_children()[-1].bind(
            "<Button-1>", lambda e: self._show_register())

    def _do_login(self):
        email = self.e_email.get().strip()
        pwd = self.e_pass.get().strip()
        if email in {"Enter your email", ""}:
            self.msg_var.set("Email is required"); return
        if pwd in {"Enter your password", ""}:
            self.msg_var.set("Password is required"); return

        user = login_user(email, pwd)
        if not user:
            messagebox.showerror("Invalid email or password")
            return
        
        messagebox.showinfo("Login successful", f"Welcome back, {user['UserName']}!")

        self.destroy()
        self.on_login(user["UserID"])

    # REGISTER FORM
    def _show_register(self):
        self._clear()
        self.geometry("1920x1080")
        self.resizable(True, True)

        hdr = tk.Frame(self, bg = C["bg_app"], pady = 28)
        hdr.pack(fill = "x")
        tk.Label(hdr, text = "💸", bg = C["bg_app"], font = ("Segoe UI", 30)).pack()
        tk.Label(hdr, text = "Create Account", bg = C["bg_app"], fg = C["text_pri"], font = ("Segoe UI", 18, "bold")).pack(pady = (4, 2))
        tk.Label(hdr, text = "Fill in your details below", bg = C["bg_app"], fg = C["text_muted"], font = FONT_SMALL).pack()

        body = tk.Frame(self, bg = C["bg_app"], padx = 40)
        body.pack(fill = "both", expand = True)

        fields = [
            ("Full Name", "Enter your full name",  False),
            ("Email", "Enter your email",       False),
            ("Phone", "Phone number (optional)", False),
            ("Password", "Create a password",      True),
            ("Confirm Password", "Confirm your password", True),
            ("Bank Name", "Enter your bank name", False),
            ("Initial Balance", "Enter initial balance (e.g. 1000)", False)
        ]

        self.reg_fields = {}
        for lbl, ph, is_pass in fields:
            tk.Label(body, text = lbl, bg = C["bg_app"],
                     fg = C["text_sec"], font = FONT_SMALL).pack(anchor = "w", pady = (10, 3))
            e = entry_field(body, ph, show = "•" if is_pass else "")
            e.pack(fill = "x", ipady = 8)
            self.reg_fields[lbl] = e

        self.reg_msg = tk.StringVar()
        tk.Label(body, textvariable = self.reg_msg, bg = C["bg_app"],
                 fg = C["danger"], font = FONT_SMALL).pack(anchor = "w", pady = (8, 0))
        
        btn(body, "Create Account", command = self._do_register,
            style = "success").pack(fill = "x", pady = (10, 0), ipady = 4)
        
        sep(body, bg = C["border_light"]).pack(fill = "x", pady = 16)

        foot = tk.Frame(body, bg = C["bg_app"])
        foot.pack(fill = "x", pady = (0, 20))
        tk.Label(foot, text = "Already have an account?", bg = C["bg_app"],
                 fg = C["text_muted"], font = FONT_SMALL).pack(side = "left")
        tk.Label(foot, text = " Sign in", bg = C["bg_app"],
                 fg = C["accent_light"], font = ("Segoe UI", 10, "bold"),
                 cursor = "hand2").pack(side = "left")
        foot.winfo_children()[-1].bind(
            "<Button-1>", lambda e: self._show_login())

    def _do_register(self):
        name = self.reg_fields["Full Name"].get().strip()
        email = self.reg_fields["Email"].get().strip()
        phone = self.reg_fields["Phone"].get().strip()
        pwd = self.reg_fields["Password"].get().strip()
        confirm_pwd = self.reg_fields["Confirm Password"].get().strip()
        bank_name = self.reg_fields["Bank Name"].get().strip()
        balance_str = self.reg_fields["Initial Balance"].get().strip()

        placeholders = {"Enter your full name", "Enter your email",
                        "Phone number (optional)", "Create a password", "Confirm your password", 
                        "Enter your bank name", "Enter initial balance (e.g. 1000)", ""}
                        
        if name in placeholders:
            self.reg_msg.set("Full name is required"); return
        if email in placeholders:
            self.reg_msg.set("Email is required"); return
        if pwd in placeholders:
            self.reg_msg.set("Password is required"); return
        if confirm_pwd in placeholders:
            self.reg_msg.set("Please confirm your password"); return
        if pwd != confirm_pwd:
            self.reg_msg.set("Passwords do not match!"); return
        if bank_name in placeholders:
            self.reg_msg.set("Bank Name is required"); return
        try:
            balance = float(balance_str)
        except ValueError:
            messagebox.showerror("Invalid input", "Initial Balance must be a valid number."); return
        
        try:
            phone_val = "" if phone in placeholders else phone
            uid = create_user(name, email, phone_val, pwd)
            
            if not uid:
                messagebox.showerror("Registration failed", "An account with this email may already exist.")
                return
            
            create_initial_account(uid, bank_name, balance)

            user = get_user_by_id(uid)
            messagebox.showinfo(f"Registration successful", f"Your account has been created. Welcome {user['FullName']}!")
            
            self.destroy()
            self.on_login(uid)
        except Exception as ex:
            messagebox.showerror("Error", f"An error occurred during registration: {ex}")