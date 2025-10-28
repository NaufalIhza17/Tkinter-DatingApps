import tkinter as tk
from tkinter import messagebox
# from tkcalendar import DateEntry  # Commented out due to navigation button issues
import json
import os
from datetime import datetime
import hashlib
import re
import calendar


class DatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dating App 💕")
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        self.root.configure(bg="#FFE5E5")

        self.current_user = None
        self.users_file = "users.json"

        # Initialize users file if it doesn't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump([], f)

        self.show_home_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_users(self):
        with open(self.users_file, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def bind_mousewheel(self, canvas):
        """Bind mousewheel scrolling to canvas"""

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_to_mousewheel)
        canvas.bind("<Leave>", _unbind_from_mousewheel)

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def validate_password(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"[a-zA-Z]", password):
            return False, "Password must include at least one letter"
        if not re.search(r"[0-9]", password):
            return False, "Password must include at least one number"
        return True, "Password is valid"

    def create_custom_date_entry(self, parent):
        """Create a custom date entry widget with working navigation"""
        
        # Main frame for the date entry
        date_frame = tk.Frame(parent, bg="#FFE5E5")
        
        # Entry field
        entry = tk.Entry(
            date_frame,
            font=("Arial", 12),
            width=20,
            relief=tk.SOLID,
            bd=2,
            justify=tk.CENTER
        )
        entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Calendar button
        cal_btn = tk.Button(
            date_frame,
            text="📅",
            font=("Arial", 12),
            bg="#FF69B4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            command=lambda: self.show_calendar_popup(entry)
        )
        cal_btn.pack(side=tk.LEFT)
        
        # Add hover effects
        cal_btn.bind("<Enter>", lambda e: cal_btn.config(bg="#FF1493"))
        cal_btn.bind("<Leave>", lambda e: cal_btn.config(bg="#FF69B4"))
        
        # Set default value to today
        today = datetime.now().strftime("%Y-%m-%d")
        entry.insert(0, today)
        
        return date_frame

    def show_calendar_popup(self, entry_widget):
        """Show a calendar popup window"""
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Select Date")
        popup.geometry("330x360")
        popup.configure(bg="#FFE5E5")
        popup.resizable(False, False)
        
        # Center the popup
        popup.transient(self.root)
        popup.grab_set()
        
        # Get current date from entry or use today
        current_date_str = entry_widget.get().strip()
        if current_date_str and len(current_date_str) == 10:
            try:
                current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
            except ValueError:
                current_date = datetime.now()
        else:
            current_date = datetime.now()
        
        # Calendar variables
        self.cal_year = current_date.year
        self.cal_month = current_date.month
        
        # Header frame
        header_frame = tk.Frame(popup, bg="#FF69B4")
        header_frame.pack(fill=tk.X)
        
        # Year navigation row
        year_frame = tk.Frame(header_frame, bg="#FF69B4")
        year_frame.pack(fill=tk.X)
        
        # Year navigation buttons
        prev_year_btn = tk.Button(
            year_frame,
            text="◀",
            font=("Arial", 12, "bold"),
            bg="#FF69B4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.change_year(popup, -1)
        )
        prev_year_btn.pack(side=tk.LEFT)
        
        year_label = tk.Label(
            year_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg="#FF69B4",
            fg="white"
        )
        year_label.pack(side=tk.LEFT, expand=True)
        
        next_year_btn = tk.Button(
            year_frame,
            text="▶",
            font=("Arial", 12, "bold"),
            bg="#FF69B4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.change_year(popup, 1)
        )
        next_year_btn.pack(side=tk.RIGHT)
        
        # Month navigation row
        month_frame = tk.Frame(header_frame, bg="#FF69B4")
        month_frame.pack(fill=tk.X)
        
        # Month navigation buttons
        prev_month_btn = tk.Button(
            month_frame,
            text="◀",
            font=("Arial", 14, "bold"),
            bg="#FF69B4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.change_month(popup, -1)
        )
        prev_month_btn.pack(side=tk.LEFT)
        
        month_label = tk.Label(
            month_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#FF69B4",
            fg="white"
        )
        month_label.pack(side=tk.LEFT, expand=True)
        
        next_month_btn = tk.Button(
            month_frame,
            text="▶",
            font=("Arial", 14, "bold"),
            bg="#FF69B4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.change_month(popup, 1)
        )
        next_month_btn.pack(side=tk.RIGHT)
        
        # Add hover effects for all buttons
        prev_year_btn.bind("<Enter>", lambda e: prev_year_btn.config(bg="#FFE5E5"))
        prev_year_btn.bind("<Leave>", lambda e: prev_year_btn.config(bg="#FF69B4"))
        next_year_btn.bind("<Enter>", lambda e: next_year_btn.config(bg="#FFE5E5"))
        next_year_btn.bind("<Leave>", lambda e: next_year_btn.config(bg="#FF69B4"))
        prev_month_btn.bind("<Enter>", lambda e: prev_month_btn.config(bg="#FFE5E5"))
        prev_month_btn.bind("<Leave>", lambda e: prev_month_btn.config(bg="#FF69B4"))
        next_month_btn.bind("<Enter>", lambda e: next_month_btn.config(bg="#FFE5E5"))
        next_month_btn.bind("<Leave>", lambda e: next_month_btn.config(bg="#FF69B4"))
        
        # Calendar frame
        cal_frame = tk.Frame(popup, bg="#FFE5E5")
        cal_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Store references for the calendar update function
        self.cal_popup = popup
        self.cal_month_label = month_label
        self.cal_year_label = year_label
        self.cal_frame = cal_frame
        self.cal_entry = entry_widget
        
        # Initial calendar display
        self.update_calendar_display()
        
        # Close button
        close_btn = tk.Button(
            popup,
            text="Close",
            font=("Arial", 12, "bold"),
            bg="#FF1493",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=popup.destroy
        )
        close_btn.pack(pady=10)
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#FF69B4"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#FF1493"))

    def change_year(self, popup, direction):
        """Change the year in the calendar"""
        self.cal_year += direction
        # Keep year within reasonable bounds (1900-2100)
        if self.cal_year < 1900:
            self.cal_year = 1900
        elif self.cal_year > 2100:
            self.cal_year = 2100
        
        self.update_calendar_display()

    def change_month(self, popup, direction):
        """Change the month in the calendar"""
        self.cal_month += direction
        if self.cal_month > 12:
            self.cal_month = 1
            self.cal_year += 1
        elif self.cal_month < 1:
            self.cal_month = 12
            self.cal_year -= 1
        
        self.update_calendar_display()

    def update_calendar_display(self):
        """Update the calendar display"""
        
        # Update year and month labels
        self.cal_year_label.config(text=str(self.cal_year))
        month_name = calendar.month_name[self.cal_month]
        self.cal_month_label.config(text=month_name)
        
        # Clear existing calendar
        for widget in self.cal_frame.winfo_children():
            widget.destroy()
        
        # Get calendar data
        cal_data = calendar.monthcalendar(self.cal_year, self.cal_month)
        
        # Days of week header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = tk.Label(
                self.cal_frame,
                text=day,
                font=("Arial", 10, "bold"),
                bg="#FFE5E5",
                fg="#FF1493",
                width=4
            )
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # Calendar days
        for week_num, week in enumerate(cal_data):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                
                day_btn = tk.Button(
                    self.cal_frame,
                    text=str(day),
                    font=("Arial", 10),
                    bg="white",
                    fg="#333",
                    relief=tk.FLAT,
                    cursor="hand2",
                    width=4,
                    height=1,
                    command=lambda d=day: self.select_date(d)
                )
                day_btn.grid(row=week_num + 1, column=day_num, padx=1, pady=1)
                
                # Add hover effects
                day_btn.bind("<Enter>", lambda e, btn=day_btn: btn.config(bg="#FFE5E5"))
                day_btn.bind("<Leave>", lambda e, btn=day_btn: btn.config(bg="white"))
        
        # Disable future dates
        today = datetime.now()
        if self.cal_year == today.year and self.cal_month == today.month:
            for widget in self.cal_frame.winfo_children():
                if isinstance(widget, tk.Button) and widget.cget("text").isdigit():
                    day = int(widget.cget("text"))
                    if day > today.day:
                        widget.config(state=tk.DISABLED, bg="#F0F0F0", fg="#999")

    def select_date(self, day):
        """Select a date from the calendar"""
        selected_date = f"{self.cal_year:04d}-{self.cal_month:02d}-{day:02d}"
        self.cal_entry.delete(0, tk.END)
        self.cal_entry.insert(0, selected_date)
        self.cal_popup.destroy()

    # HOME PAGE
    def show_home_page(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#FFE5E5")
        frame.pack(fill=tk.BOTH, expand=True)

        # Cat emoji header
        tk.Label(frame, text="🐱", font=("Arial", 80), bg="#FFE5E5").pack(pady=(80, 10))

        tk.Label(
            frame,
            text="Purrfect Match",
            font=("Arial", 40, "bold"),
            bg="#FFE5E5",
            fg="#FF1493",
        ).pack(pady=5)

        tk.Label(
            frame,
            text="Find your purrfect partner! 💕",
            font=("Arial", 14),
            bg="#FFE5E5",
            fg="#FF69B4",
        ).pack(pady=10)

        # Button container
        btn_frame = tk.Frame(frame, bg="#FFE5E5")
        btn_frame.pack(pady=40)

        login_btn = tk.Button(
            btn_frame,
            text="🔐 Login",
            font=("Arial", 18, "bold"),
            bg="#FF1493",
            fg="white",
            width=18,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#FF69B4",
            activeforeground="white",
            command=self.show_login_page,
        )
        login_btn.pack(pady=15)
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#FF69B4"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#FF1493"))

        register_btn = tk.Button(
            btn_frame,
            text="✨ Register",
            font=("Arial", 18, "bold"),
            bg="#FF1493",
            fg="white",
            width=18,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#FF69B4",
            activeforeground="white",
            command=self.show_register_page,
        )
        register_btn.pack(pady=15)
        register_btn.bind("<Enter>", lambda e: register_btn.config(bg="#FF69B4"))
        register_btn.bind("<Leave>", lambda e: register_btn.config(bg="#FF1493"))

        tk.Label(
            frame, text="🐾 🐾 🐾", font=("Arial", 20), bg="#FFE5E5", fg="#FF69B4"
        ).pack(side=tk.BOTTOM, pady=30)

    # LOGIN PAGE
    def show_login_page(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#FFE5E5")
        frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(frame, bg="#FF69B4")
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="🐱 Login",
            font=("Arial", 28, "bold"),
            bg="#FF69B4",
            fg="white",
            pady=20,
        ).pack()

        # Content - centered container
        content = tk.Frame(frame, bg="#FFE5E5")
        content.pack(fill=tk.BOTH, expand=True)
        
        # Center frame for the form
        center_frame = tk.Frame(content, bg="#FFE5E5")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center_frame,
            text="Welcome back! 💕",
            font=("Arial", 16),
            bg="#FFE5E5",
            fg="#FF1493",
        ).pack(pady=(0, 30))

        # Email
        email_frame = tk.Frame(center_frame, bg="#FFE5E5")
        email_frame.pack(fill=tk.X, pady=10)
        tk.Label(
            email_frame,
            text="📧 Email",
            font=("Arial", 13, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        email_entry = tk.Entry(
            email_frame, font=("Arial", 13), width=40, relief=tk.SOLID, bd=2
        )
        email_entry.pack(pady=8, ipady=10)

        # Password
        pass_frame = tk.Frame(center_frame, bg="#FFE5E5")
        pass_frame.pack(fill=tk.X, pady=10)
        tk.Label(
            pass_frame,
            text="🔒 Password",
            font=("Arial", 13, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        password_entry = tk.Entry(
            pass_frame, font=("Arial", 13), width=40, show="•", relief=tk.SOLID, bd=2
        )
        password_entry.pack(pady=8, ipady=10)

        # Buttons
        btn_frame = tk.Frame(center_frame, bg="#FFE5E5")
        btn_frame.pack(pady=30)

        submit_btn = tk.Button(
            btn_frame,
            text="Login 🚀",
            font=("Arial", 15, "bold"),
            bg="#FF69B4",
            fg="white",
            width=20,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=lambda: self.login(email_entry.get(), password_entry.get()),
        )
        submit_btn.pack(pady=10)

        back_btn = tk.Button(
            btn_frame,
            text="← Back",
            font=("Arial", 12),
            bg="#DDD",
            fg="#333",
            width=20,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_home_page,
        )
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#CCC"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#DDD"))

        def check_fields(*args):
            if email_entry.get().strip() and password_entry.get().strip():
                submit_btn.config(state=tk.NORMAL, cursor="hand2")
            else:
                submit_btn.config(state=tk.DISABLED, cursor="arrow")

        email_entry.bind("<KeyRelease>", check_fields)
        password_entry.bind("<KeyRelease>", check_fields)

    def login(self, email, password):
        users = self.load_users()
        hashed_password = self.hash_password(password)

        for user in users:
            if user["email"] == email and user["password"] == hashed_password:
                self.current_user = user
                messagebox.showinfo("Success! 🎉", "Login successful! Welcome back! 💕")
                self.show_main_page()
                return

        messagebox.showerror("Oops! 😿", "Invalid email or password!")

    # REGISTER PAGE
    def show_register_page(self):
        self.clear_window()

        # Main container
        main_frame = tk.Frame(self.root, bg="#FFE5E5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(main_frame, bg="#FF1493")
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="✨ Create Account",
            font=("Arial", 28, "bold"),
            bg="#FF1493",
            fg="white",
            pady=20,
        ).pack()

        # Scrollable content
        canvas = tk.Canvas(main_frame, bg="#FFE5E5", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFE5E5")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mousewheel
        self.bind_mousewheel(canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content = tk.Frame(scrollable_frame, bg="#FFE5E5")
        content.pack(padx=80, pady=40)

        tk.Label(
            content,
            text="Join the fun! 🐾",
            font=("Arial", 16),
            bg="#FFE5E5",
            fg="#FF1493",
        ).pack(pady=(0, 20))

        # Full Name
        name_frame = tk.Frame(content, bg="#FFE5E5")
        name_frame.pack(fill=tk.X, pady=8)
        tk.Label(
            name_frame,
            text="👤 Full Name",
            font=("Arial", 12, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        fullname_entry = tk.Entry(
            name_frame, font=("Arial", 12), width=45, relief=tk.SOLID, bd=2
        )
        fullname_entry.pack(pady=5, ipady=8)

        # Email
        email_frame = tk.Frame(content, bg="#FFE5E5")
        email_frame.pack(fill=tk.X, pady=8)
        tk.Label(
            email_frame,
            text="📧 Email",
            font=("Arial", 12, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        email_entry = tk.Entry(
            email_frame, font=("Arial", 12), width=45, relief=tk.SOLID, bd=2
        )
        email_entry.pack(pady=5, ipady=8)
        email_warning = tk.Label(
            email_frame, text="", font=("Arial", 9), bg="#FFE5E5", fg="#FF0000"
        )
        email_warning.pack(anchor=tk.W)

        # Password
        pass_frame = tk.Frame(content, bg="#FFE5E5")
        pass_frame.pack(fill=tk.X, pady=8)
        tk.Label(
            pass_frame,
            text="🔒 Password",
            font=("Arial", 12, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        password_entry = tk.Entry(
            pass_frame, font=("Arial", 12), width=45, show="•", relief=tk.SOLID, bd=2
        )
        password_entry.pack(pady=5, ipady=8)
        password_warning = tk.Label(
            pass_frame, text="", font=("Arial", 9), bg="#FFE5E5", fg="#FF0000"
        )
        password_warning.pack(anchor=tk.W)

        # Gender
        gender_frame = tk.Frame(content, bg="#FFE5E5")
        gender_frame.pack(fill=tk.X, pady=8)
        tk.Label(
            gender_frame,
            text="⚧ Gender",
            font=("Arial", 12, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        gender_var = tk.StringVar(value="")
        radio_frame = tk.Frame(gender_frame, bg="#FFE5E5")
        radio_frame.pack(anchor=tk.W, pady=8)
        tk.Radiobutton(
            radio_frame,
            text="♂ Male",
            variable=gender_var,
            value="Male",
            font=("Arial", 11),
            bg="#FFE5E5",
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=15)
        tk.Radiobutton(
            radio_frame,
            text="♀ Female",
            variable=gender_var,
            value="Female",
            font=("Arial", 11),
            bg="#FFE5E5",
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=15)

        # Date of Birth
        dob_frame = tk.Frame(content, bg="#FFE5E5")
        dob_frame.pack(fill=tk.X, pady=8)
        tk.Label(
            dob_frame,
            text="🎂 Date of Birth",
            font=("Arial", 12, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        # Custom date entry with working navigation
        dob_entry = self.create_custom_date_entry(dob_frame)
        dob_entry.pack(pady=5, ipady=2)

        # Gender Interest
        interest_frame = tk.Frame(content, bg="#FFE5E5")
        interest_frame.pack(fill=tk.X, pady=8)
        tk.Label(
            interest_frame,
            text="💕 Interested in",
            font=("Arial", 12, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        check_frame = tk.Frame(interest_frame, bg="#FFE5E5")
        check_frame.pack(anchor=tk.W, pady=8)
        male_interest = tk.BooleanVar()
        female_interest = tk.BooleanVar()
        tk.Checkbutton(
            check_frame,
            text="♂ Male",
            variable=male_interest,
            font=("Arial", 11),
            bg="#FFE5E5",
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=15)
        tk.Checkbutton(
            check_frame,
            text="♀ Female",
            variable=female_interest,
            font=("Arial", 11),
            bg="#FFE5E5",
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=15)

        # Bio
        bio_frame = tk.Frame(content, bg="#FFE5E5")
        bio_frame.pack(fill=tk.X, pady=8)
        tk.Label(
            bio_frame,
            text="✍️ About You",
            font=("Arial", 12, "bold"),
            bg="#FFE5E5",
            fg="#333",
        ).pack(anchor=tk.W)
        bio_text = tk.Text(
            bio_frame,
            font=("Arial", 11),
            width=45,
            height=5,
            relief=tk.SOLID,
            bd=2,
            wrap=tk.WORD,
        )
        bio_text.pack(pady=5)

        # Submit Button
        btn_frame = tk.Frame(content, bg="#FFE5E5")
        btn_frame.pack(pady=25)

        submit_btn = tk.Button(
            btn_frame,
            text="Register ✨",
            font=("Arial", 15, "bold"),
            bg="#FF1493",
            fg="white",
            width=25,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=lambda: self.register(
                fullname_entry.get(),
                email_entry.get(),
                password_entry.get(),
                gender_var.get(),
                dob_entry.winfo_children()[0].get(),  # Get date from the entry field
                male_interest.get(),
                female_interest.get(),
                bio_text.get("1.0", tk.END).strip(),
            ),
        )
        submit_btn.pack(pady=10)

        back_btn = tk.Button(
            btn_frame,
            text="← Back",
            font=("Arial", 12),
            bg="#DDD",
            fg="#333",
            width=25,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_home_page,
        )
        back_btn.pack(pady=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#CCC"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#DDD"))

        def check_email(*args):
            email = email_entry.get().strip()
            if email and not self.validate_email(email):
                email_warning.config(
                    text="⚠️ Please enter a valid email format (example@mail.com)"
                )
                return False
            else:
                email_warning.config(text="")
                return True

        def check_password(*args):
            password = password_entry.get().strip()
            if password:
                valid, message = self.validate_password(password)
                if not valid:
                    password_warning.config(text=f"⚠️ {message}")
                    return False
                else:
                    password_warning.config(text="")
                    return True
            else:
                password_warning.config(text="")
                return False

        def check_fields(*args):
            email_valid = check_email()
            password_valid = check_password()

            if (
                fullname_entry.get().strip()
                and email_entry.get().strip()
                and password_entry.get().strip()
                and gender_var.get()
                and (male_interest.get() or female_interest.get())
                and bio_text.get("1.0", tk.END).strip()
                and email_valid
                and password_valid
            ):
                submit_btn.config(state=tk.NORMAL, cursor="hand2")
            else:
                submit_btn.config(state=tk.DISABLED, cursor="arrow")

        fullname_entry.bind("<KeyRelease>", check_fields)
        email_entry.bind("<KeyRelease>", check_fields)
        password_entry.bind("<KeyRelease>", check_fields)
        gender_var.trace("w", check_fields)
        male_interest.trace("w", check_fields)
        female_interest.trace("w", check_fields)
        bio_text.bind("<KeyRelease>", check_fields)

    def register(
        self,
        fullname,
        email,
        password,
        gender,
        dob,
        male_interest,
        female_interest,
        bio,
    ):
        users = self.load_users()

        # Check if email already exists
        for user in users:
            if user["email"] == email:
                messagebox.showerror("Oops! 😿", "Email already registered!")
                return

        interests = []
        if male_interest:
            interests.append("Male")
        if female_interest:
            interests.append("Female")

        new_user = {
            "fullname": fullname,
            "email": email,
            "password": self.hash_password(password),
            "gender": gender,
            "dob": dob,
            "interests": interests,
            "bio": bio,
        }

        users.append(new_user)
        self.save_users(users)

        messagebox.showinfo("Success! 🎉", "Registration successful! Please login. 💕")
        self.show_login_page()

    # MAIN PAGE
    def show_main_page(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#FFE5E5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(main_frame, bg="#FF69B4")
        header.pack(fill=tk.X)

        header_content = tk.Frame(header, bg="#FF69B4")
        header_content.pack(fill=tk.X, padx=30, pady=15)

        tk.Label(
            header_content,
            text=f"🐱 Welcome, {self.current_user['fullname']}!",
            font=("Arial", 20, "bold"),
            bg="#FF69B4",
            fg="white",
        ).pack(side=tk.LEFT)

        logout_btn = tk.Button(
            header_content,
            text="Logout 👋",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#FF1493",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=self.logout,
        )
        logout_btn.pack(side=tk.RIGHT)
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#FFE5E5"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="white"))

        # Scrollable content
        canvas = tk.Canvas(main_frame, bg="#FFE5E5", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFE5E5")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scrollbar.set)

        self.bind_mousewheel(canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Content
        content = tk.Frame(scrollable_frame, bg="#FFE5E5")
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        tk.Label(
            content,
            text="💕 Your Matches",
            font=("Arial", 22, "bold"),
            bg="#FFE5E5",
            fg="#FF1493",
        ).pack(pady=(0, 5))

        # User info
        interests_text = " & ".join(self.current_user["interests"])
        tk.Label(
            content,
            text=f"You are a {self.current_user['gender']} looking for {interests_text}",
            font=("Arial", 12, "italic"),
            bg="#FFE5E5",
            fg="#666",
        ).pack(pady=(0, 20))

        # Load matching users
        users = self.load_users()
        matches = []
        for user in users:
            if (
                user["email"] != self.current_user["email"]
                and user["gender"] in self.current_user["interests"]
            ):
                matches.append(user)

        if len(matches) == 0:
            # No matches message
            no_match_frame = tk.Frame(content, bg="white", relief=tk.SOLID, bd=2)
            no_match_frame.pack(pady=50, padx=50)

            tk.Label(no_match_frame, text="😿", font=("Arial", 60), bg="white").pack(
                pady=(30, 10)
            )
            tk.Label(
                no_match_frame,
                text="No matches found yet!",
                font=("Arial", 18, "bold"),
                bg="white",
                fg="#FF1493",
            ).pack(pady=5)
            tk.Label(
                no_match_frame,
                text="Come back later for more purrfect matches! 🐾",
                font=("Arial", 12),
                bg="white",
                fg="#666",
            ).pack(pady=(5, 30), padx=30)
        else:
            # Create grid of cards
            cards_frame = tk.Frame(content, bg="#FFE5E5")
            cards_frame.pack(fill=tk.BOTH, expand=True)

            row = 0
            col = 0
            for user in matches:
                self.create_user_card(cards_frame, user, row, col)
                col += 1
                if col >= 2:
                    col = 0
                    row += 1

    def create_user_card(self, parent, user, row, col):
        # Card container
        card = tk.Frame(parent, bg="white", relief=tk.SOLID, bd=2, cursor="hand2")
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        # Card content with padding
        content = tk.Frame(card, bg="white")
        content.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Avatar
        gender_emoji = "♂️" if user["gender"] == "Male" else "♀️"
        tk.Label(content, text="🐱", font=("Arial", 40), bg="white").pack(pady=(0, 5))

        # Name
        tk.Label(
            content,
            text=user["fullname"],
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#FF1493",
        ).pack(pady=5)

        # Gender badge
        gender_bg = "#ADD8E6" if user["gender"] == "Male" else "#FFB6C1"
        gender_frame = tk.Frame(content, bg=gender_bg, relief=tk.SOLID, bd=1)
        gender_frame.pack(pady=5)
        tk.Label(
            gender_frame,
            text=f"{gender_emoji} {user['gender']}",
            font=("Arial", 10, "bold"),
            bg=gender_bg,
            fg="white",
            padx=10,
            pady=2,
        ).pack()

        # Age
        dob = datetime.strptime(user["dob"], "%Y-%m-%d")
        age = datetime.now().year - dob.year
        tk.Label(
            content,
            text=f"🎂 {age} years old",
            font=("Arial", 11),
            bg="white",
            fg="#666",
        ).pack(pady=5)

        # Bio preview (truncated)
        bio_preview = user["bio"][:60] + "..." if len(user["bio"]) > 60 else user["bio"]
        tk.Label(
            content,
            text=bio_preview,
            font=("Arial", 10),
            bg="white",
            fg="#888",
            wraplength=250,
            justify=tk.LEFT,
        ).pack(pady=10)

        # View details button
        view_btn = tk.Button(
            content,
            text="View Profile 👀",
            font=("Arial", 10, "bold"),
            bg="#FF69B4",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=5,
            command=lambda: self.show_user_details(user["email"]),
        )
        view_btn.pack(pady=(10, 0))
        view_btn.bind("<Enter>", lambda e: view_btn.config(bg="#FF1493"))
        view_btn.bind("<Leave>", lambda e: view_btn.config(bg="#FF69B4"))

        # Hover effect for card
        def on_enter(e):
            card.config(bg="#FFB6C1", bd=3)
            content.config(bg="#FFB6C1")
            for widget in content.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="#FFB6C1")

        def on_leave(e):
            card.config(bg="white", bd=2)
            content.config(bg="white")
            for widget in content.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg="white")
                elif isinstance(widget, tk.Frame) and widget != gender_frame:
                    widget.config(bg="white")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        content.bind("<Enter>", on_enter)
        content.bind("<Leave>", on_leave)

    def show_user_details(self, email):
        users = self.load_users()
        user = next((u for u in users if u["email"] == email), None)

        if user:
            dob = datetime.strptime(user["dob"], "%Y-%m-%d")
            age = datetime.now().year - dob.year

            details = f"""
🐱 Name: {user["fullname"]}

📧 Email: {user["email"]}

⚧ Gender: {user["gender"]}

🎂 Date of Birth: {user["dob"]}

🎈 Age: {age} years old

✍️ Bio: 
{user["bio"]}
            """
            messagebox.showinfo("Profile Details 💕", details.strip())

    def logout(self):
        self.current_user = None
        self.show_home_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = DatingApp(root)
    root.mainloop()
