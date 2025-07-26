import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
import hashlib
import smtplib
import random
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# NEW: Folder and file paths setup
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "secure_notepad_data")
os.makedirs(DATA_DIR, exist_ok=True)  # Auto-create folder

USER_DATA_PATH = os.path.join(DATA_DIR, "user_data.json")
NOTES_DATA_PATH = os.path.join(DATA_DIR, "notes_data.json")
KEY_FILE_PATH = os.path.join(DATA_DIR, "secret.key")

class SecureNotepad:
    def __init__(self):
        self.fernet = self._initialize_encryption()
        self.window = self._setup_window()
        self.current_user = None
        self._show_welcome_screen()
        self.window.mainloop()

    # ======================
    # Security Methods
    # ======================
    def _initialize_encryption(self):
        """Handles encryption key creation/loading"""
        if os.path.exists(KEY_FILE_PATH):
            with open(KEY_FILE_PATH, "rb") as f:
                return Fernet(f.read())
        key = Fernet.generate_key()
        with open(KEY_FILE_PATH, "wb") as f:
            f.write(key)
        return Fernet(key)

    def _hash_password(self, password):
        """Securely hashes passwords using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _send_otp(self, email):
        """Sends OTP via SMTP with environment variables"""
        sender_email = os.getenv("VAULT_EMAIL")
        sender_pass = os.getenv("VAULT_EMAIL_PASSWORD")
        
        if not all([sender_email, sender_pass]):
            messagebox.showerror("Configuration Error", 
                               "Email credentials not properly configured")
            return None

        otp = str(random.randint(100000, 999999))
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_pass)
                server.sendmail(
                    sender_email,
                    email,
                    f"Subject: Secure Notepad OTP\n\nYour OTP is: {otp}"
                )
            return otp
        except Exception as e:
            messagebox.showerror("Email Error", 
                                f"Failed to send OTP:\n{str(e)}")
            return None

    # ======================
    # UI Screens
    # ======================
    def _setup_window(self):
        """Configures main application window"""
        window = tk.Tk()
        window.title("Secure Notepad v2.0")
        window.geometry("500x450")
        window.configure(bg="#f0f8ff")
        window.resizable(False, False)
        return window

    def _clear_screen(self):
        """Clears all widgets from window"""
        for widget in self.window.winfo_children():
            widget.destroy()

    def _show_welcome_screen(self):
        """Initial welcome/authentication screen"""
        self._clear_screen()
        
        tk.Label(
            self.window, 
            text="🔒 Secure Notepad", 
            font=("Arial", 20, "bold"),
            bg="#f0f8ff"
        ).pack(pady=30)

        action_frame = tk.Frame(self.window, bg="#f0f8ff")
        action_frame.pack(pady=20)

        buttons = [
            ("Login", "#4CAF50", self._show_login_screen),
            ("Sign Up", "#2196F3", self._show_signup_screen),
            ("Exit", "#f44336", self.window.quit)
        ]

        for text, color, command in buttons:
            tk.Button(
                action_frame,
                text=text,
                width=15,
                font=("Arial", 12),
                bg=color,
                fg="white",
                command=command
            ).pack(pady=8, padx=10)

    def _show_signup_screen(self):
        """User registration screen"""
        self._clear_screen()
        
        tk.Label(
            self.window,
            text="Create Account",
            font=("Arial", 18),
            bg="#f0f8ff"
        ).pack(pady=20)

        entries = {}
        fields = [
            ("Username", "username"),
            ("Email", "email"), 
            ("Password", "password", True),
            ("Confirm Password", "confirm", True)
        ]

        for field in fields:
            label_text = field[0]
            field_name = field[1]
            show_char = "*" if len(field) > 2 else ""
            
            tk.Label(
                self.window,
                text=label_text + ":",
                font=("Arial", 10),
                bg="#f0f8ff"
            ).pack()
            
            entries[field_name] = tk.Entry(
                self.window,
                width=30,
                show=show_char
            )
            entries[field_name].pack(pady=5)

        self.signup_entries = entries

        tk.Button(
            self.window,
            text="Register",
            width=20,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self._handle_signup
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="← Back",
            command=self._show_welcome_screen
        ).pack()

    def _show_login_screen(self):
        """User login screen"""
        self._clear_screen()
        
        tk.Label(
            self.window,
            text="Login",
            font=("Arial", 18),
            bg="#f0f8ff"
        ).pack(pady=20)

        # Username dropdown
        usernames = []
        if os.path.exists(USER_DATA_PATH):
            with open(USER_DATA_PATH, "r") as f:
                usernames = list(json.load(f).keys())

        tk.Label(
            self.window,
            text="Username:",
            font=("Arial", 10),
            bg="#f0f8ff"
        ).pack()
        
        self.username_combo = ttk.Combobox(
            self.window,
            values=usernames,
            state="readonly",
            width=27
        )
        self.username_combo.pack(pady=5)

        # Password entry
        tk.Label(
            self.window,
            text="Password:",
            font=("Arial", 10),
            bg="#f0f8ff"
        ).pack()
        
        self.password_entry = tk.Entry(
            self.window,
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.window,
            text="Login",
            width=20,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self._handle_login
        ).pack(pady=20)

        tk.Button(
            self.window,
            text="← Back",
            command=self._show_welcome_screen
        ).pack()

    def _show_notepad(self):
        """Main notepad interface"""
        self._clear_screen()
        
        # Header
        header = tk.Frame(self.window, bg="#e3f2fd")
        header.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(
            header,
            text=f"User: {self.current_user}",
            font=("Arial", 10, "bold"),
            bg="#e3f2fd"
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header,
            text="Logout",
            command=self._show_welcome_screen,
            bg="#f44336",
            fg="white"
        ).pack(side=tk.RIGHT)

        # Text area
        self.text_area = tk.Text(
            self.window,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Arial", 11)
        )
        self.text_area.pack(pady=10, padx=10)

        # Load existing note
        self._load_note()

        # Button controls
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Save",
            command=self._save_note,
            bg="#4CAF50",
            fg="white",
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Clear",
            command=self._clear_note,
            bg="#ff9800",
            fg="white",
            width=10
        ).pack(side=tk.LEFT, padx=5)

    # ======================
    # Core Functionality
    # ======================
    def _handle_signup(self):
        """Processes new user registration"""
        username = self.signup_entries["username"].get().strip()
        email = self.signup_entries["email"].get().strip().lower()
        password = self.signup_entries["password"].get()
        confirm = self.signup_entries["confirm"].get()

        # Validation
        if not all([username, email, password, confirm]):
            messagebox.showwarning("Error", "All fields are required!")
            return
            
        if password != confirm:
            messagebox.showwarning("Error", "Passwords don't match!")
            return
            
        if "@" not in email or "." not in email:
            messagebox.showwarning("Error", "Invalid email format!")
            return

        # Check existing users
        users = {}
        if os.path.exists(USER_DATA_PATH):
            with open(USER_DATA_PATH, "r") as f:
                users = json.load(f)

        if username in users:
            messagebox.showwarning("Error", "Username already exists!")
            return
            
        if any(user["email"] == email for user in users.values()):
            messagebox.showwarning("Error", "Email already registered!")
            return

        # OTP Verification
        otp = self._send_otp(email)
        if not otp:
            return
            
        user_otp = simpledialog.askstring("OTP Verification", 
                                         "Enter the OTP sent to your email:")
        if user_otp != otp:
            messagebox.showerror("Error", "Invalid OTP!")
            return

        # Save new user
        users[username] = {
            "email": email,
            "password": self._hash_password(password)
        }
        
        with open(USER_DATA_PATH, "w") as f:
            json.dump(users, f, indent=4)

        # Initialize empty note
        self._initialize_user_note(username)
        
        messagebox.showinfo("Success", "Account created successfully!")
        self.current_user = username
        self._show_notepad()

    def _handle_login(self):
        """Authenticates existing users"""
        username = self.username_combo.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Error", "Both fields are required!")
            return

        try:
            with open(USER_DATA_PATH, "r") as f:
                users = json.load(f)
                
            if username in users and users[username]["password"] == self._hash_password(password):
                self.current_user = username
                self._show_notepad()
            else:
                messagebox.showerror("Error", "Invalid credentials!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Login failed:\n{str(e)}")

    def _initialize_user_note(self, username):
        """Creates empty encrypted note for new user"""
        notes = {}
        if os.path.exists(NOTES_DATA_PATH):
            with open(NOTES_DATA_PATH, "r") as f:
                notes = json.load(f)
                
        notes[username] = self.fernet.encrypt(b"").decode()
        
        with open(NOTES_DATA_PATH, "w") as f:
            json.dump(notes, f, indent=4)

    def _load_note(self):
        """Decrypts and loads user's note"""
        if not os.path.exists(NOTES_DATA_PATH):
            return
            
        with open(NOTES_DATA_PATH, "r") as f:
            notes = json.load(f)
            
        encrypted_note = notes.get(self.current_user, "")
        if encrypted_note:
            try:
                decrypted = self.fernet.decrypt(encrypted_note.encode()).decode()
                self.text_area.insert(tk.END, decrypted)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt note:\n{str(e)}")

    def _save_note(self):
        """Encrypts and saves the current note"""
        note_content = self.text_area.get("1.0", tk.END).strip()
        encrypted = self.fernet.encrypt(note_content.encode()).decode()
        
        notes = {}
        if os.path.exists(NOTES_DATA_PATH):
            with open(NOTES_DATA_PATH, "r") as f:
                notes = json.load(f)
                
        notes[self.current_user] = encrypted
        
        with open(NOTES_DATA_PATH, "w") as f:
            json.dump(notes, f, indent=4)
            
        messagebox.showinfo("Saved", "Note encrypted and saved successfully!")

    def _clear_note(self):
        """Clears the current note"""
        if messagebox.askyesno("Confirm", "Clear all text?"):
            self.text_area.delete("1.0", tk.END)
            self._save_note()

if __name__ == "__main__":
    SecureNotepad()