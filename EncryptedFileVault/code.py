import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog
import hashlib
import smtplib
import json
import os
import random
import re
import shutil
import datetime
from cryptography.fernet import Fernet
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ======================
# Configuration
# ======================
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "secure_data")
VAULT_DIR = os.path.join(DATA_DIR, "vault")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VAULT_DIR, exist_ok=True)

USERDATA_PATH = os.path.join(DATA_DIR, "userdata.json")

# Verify .env configuration
if not all([os.getenv("VAULT_EMAIL"), os.getenv("VAULT_EMAIL_PASSWORD")]):
    messagebox.showerror("Configuration Error",
                       "Missing email credentials in .env file\n\n"
                       "Please create a .env file with:\n"
                       "VAULT_EMAIL=your@email.com\n"
                       "VAULT_EMAIL_PASSWORD=your_app_password")
    exit()

# ======================
# Helper Functions
# ======================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_otp_to_email(email):
    otp = str(random.randint(100000, 999999))
    sender_email = os.getenv("VAULT_EMAIL")
    sender_pass = os.getenv("VAULT_EMAIL_PASSWORD")

    subject = "Your OTP Verification Code"
    message = f"Subject: {subject}\n\nYour OTP is: {otp}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, email, message)
        return otp
    except Exception as e:
        messagebox.showerror("Email Error", f"❌ Could not send OTP:\n{e}")
        return None

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def load_user_data():
    try:
        if os.path.exists(USERDATA_PATH):
            with open(USERDATA_PATH, "r") as f:
                return json.load(f) or {}
        return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# ======================
# Main Application
# ======================
class MainPage:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.current_password = None
        self.cipher_suite = None
        
        # UI Setup
        self.root.title("Secure File Vault")
        self.root.geometry("600x500")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(bg="#dce3f0")
        self.root.resizable(False, False)
        
        self.create_widgets()
    
    def generate_key(self, password):
        key = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key)

    def setup_encryption(self, password):
        key = self.generate_key(password)
        self.cipher_suite = Fernet(key)

    def encrypt_content(self, content):
        if isinstance(content, str):
            content = content.encode()
        return self.cipher_suite.encrypt(content)

    def decrypt_content(self, encrypted_content):
        return self.cipher_suite.decrypt(encrypted_content).decode()

    def hash_filename(self, filename):
        return hashlib.sha256(filename.encode()).hexdigest()

    def open_signup(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        back_btn = ctk.CTkButton(self.root, text="← Back", width=80, fg_color="#6B7280",
                                hover_color="#4B5563", font=("Segoe UI", 12),
                                command=self.create_widgets)
        back_btn.place(x=20, y=20)

        heading = ctk.CTkLabel(self.root, text="Create Your Account",
                             font=ctk.CTkFont(size=22, weight="bold"))
        heading.pack(pady=(60, 20))

        self.username_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter username")
        self.username_entry.pack(pady=5)

        self.email_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter email")
        self.email_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter password", show="*")
        self.password_entry.pack(pady=5)

        self.confirm_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Re-enter password", show="*")
        self.confirm_entry.pack(pady=5)

        submit_btn = ctk.CTkButton(self.root, text="Submit", width=150, fg_color="#10B981",
                                 hover_color="#059669", command=self.submit_signup)
        submit_btn.pack(pady=20)

    def submit_signup(self):
        uname = self.username_entry.get().strip()
        email = self.email_entry.get().strip().lower()
        pwd = self.password_entry.get().strip()
        confirm_pwd = self.confirm_entry.get().strip()

        # Validation checks
        if not uname or not email or not pwd or not confirm_pwd:
            messagebox.showerror("Error", "⚠️ Please fill all fields.")
            return
        if len(pwd) < 8 or not any(c.isupper() for c in pwd) or not any(c.isdigit() for c in pwd):
            messagebox.showerror("Weak Password", "Use 8+ chars with uppercase, numbers")
            return

        if pwd != confirm_pwd:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        # Check for existing users
        users = load_user_data()
        if not isinstance(users, dict):
            users = {}

        if uname in users:
            messagebox.showerror("Duplicate", "Username already exists.")
            return

        if any(data.get("email") == email for data in users.values() if isinstance(data, dict)):
            messagebox.showerror("Duplicate", "Email already registered.")
            return

        # OTP Verification
        otp_sent = send_otp_to_email(email)
        if not otp_sent:
            return

        otp_entered = simpledialog.askstring("OTP Verification", 
                                            "Enter the 6-digit OTP sent to your email:",
                                            show="*")
        if otp_entered is None or otp_entered != otp_sent:
            messagebox.showerror("Incorrect OTP", "OTP did not match. Signup failed.")
            return

        # Secure account creation
        try:
            # Create user vault directory
            user_vault_dir = os.path.join(VAULT_DIR, uname)
            os.makedirs(user_vault_dir, exist_ok=True)

            # Hash password and store user data
            hashed_pwd = hash_password(pwd)
            users[uname] = {
                "email": email,
                "password": hashed_pwd,
                "created_at": datetime.datetime.now().isoformat()
            }

            # Save user data
            with open(USERDATA_PATH, "w") as f:
                json.dump(users, f, indent=4)

            # Initialize encryption for the session
            self.current_user = uname
            self.current_password = pwd
            self.setup_encryption(pwd)

            # Create secure filename mapping file
            mapping_path = os.path.join(user_vault_dir, ".filenames.json")
            with open(mapping_path, "w") as f:
                json.dump({}, f)

            messagebox.showinfo("Success", f"""
Account created successfully for {uname}!
• Your files will be securely encrypted
• Remember your password - it cannot be recovered
""")
            self.open_vault()

        except Exception as e:
            messagebox.showerror("Error", f"Account creation failed:\n{str(e)}")
            # Clean up if partial creation occurred
            if os.path.exists(user_vault_dir):
                shutil.rmtree(user_vault_dir)
            if uname in users:
                del users[uname]

    def reset(self):
        email = simpledialog.askstring("Forgot Password", "Enter your registered email:")
        if not email:
            return

        try:
            users = load_user_data()
            if not users or not isinstance(users, dict):
                messagebox.showerror("Error", "⚠️ No valid user data found. Please sign up first.")
                return

            username_found = None
            for uname, data in users.items():
                if isinstance(data, dict) and data.get("email") == email.lower():
                    username_found = uname
                    break

            if not username_found:
                messagebox.showerror("Error", "❌ Email not registered. Please sign up first.")
                return

            otp_sent = send_otp_to_email(email)
            if not otp_sent:
                return

            otp_entered = simpledialog.askstring("OTP Verification", "Enter the OTP sent to your email:")
            if otp_entered is None or otp_entered != otp_sent:
                messagebox.showerror("Incorrect OTP", "❌ OTP did not match. Try again.")
                return

            new_pwd = simpledialog.askstring("Reset Password", "Enter your new password:", show="*")
            confirm_pwd = simpledialog.askstring("Confirm Password", "Re-enter your new password:", show="*")

            if not new_pwd or not confirm_pwd:
                messagebox.showerror("Error", "⚠️ Please fill both password fields.")
                return

            if new_pwd != confirm_pwd:
                messagebox.showerror("Mismatch", "❌ Passwords do not match.")
                return

            users[username_found]["password"] = hash_password(new_pwd)

            try:
                with open(USERDATA_PATH, "w") as f:
                    json.dump(users, f, indent=4)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save password: {e}")
                return

            messagebox.showinfo("Success", "✅ Password has been reset successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def open_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        back_btn = ctk.CTkButton(self.root, text="← Back", width=80, fg_color="#6B7280",
                                hover_color="#4B5563", font=("Segoe UI", 12),
                                command=self.create_widgets)
        back_btn.place(x=20, y=20)

        heading = ctk.CTkLabel(self.root, text="Login to Your Account",
                             font=ctk.CTkFont(size=22, weight="bold"))
        heading.pack(pady=(60, 20))

        self.login_email_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter your email")
        self.login_email_entry.pack(pady=5)

        self.login_password_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter password", show="*")
        self.login_password_entry.pack(pady=5)

        login_btn = ctk.CTkButton(self.root, text="Login", width=150,
                                fg_color="#3B82F6", hover_color="#1D4ED8",
                                command=self.perform_login)
        login_btn.pack(pady=20)

        forgot_btn = ctk.CTkButton(self.root, text="Forgot Password?", width=180,
                                 fg_color="#9CA3AF", hover_color="#6B7280",
                                 command=self.reset)
        forgot_btn.pack(pady=10)

    def perform_login(self):
        email = self.login_email_entry.get().strip().lower()
        pwd = self.login_password_entry.get().strip()

        if not email or not pwd:
            messagebox.showerror("Error", "⚠️ Please fill all fields.")
            return

        users = load_user_data()
        if not users or not isinstance(users, dict):
            messagebox.showerror("Error", "No valid user data found. Please sign up first.")
            return

        for uname, data in users.items():
            if isinstance(data, dict) and data.get("email") == email:
                if data.get("password") == hash_password(pwd):
                    self.current_user = uname
                    self.current_password = pwd
                    self.setup_encryption(pwd)
                    messagebox.showinfo("Success", f"✅ Logged in as {uname}")
                    self.open_vault()
                    return
                else:
                    messagebox.showerror("Error", "❌ Incorrect password.")
                    return

        messagebox.showerror("Error", "❌ Email not registered.")

    def open_text_editor(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        back_btn = ctk.CTkButton(
            self.root,
            text="← Back",
            width=80,
            fg_color="#6B7280",
            hover_color="#4B5563",
            font=("Segoe UI", 12),
            command=lambda: self.open_vault()
        )
        back_btn.place(x=20, y=20)

        heading = ctk.CTkLabel(
            self.root,
            text="✍️ Write Your File",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        heading.pack(pady=(60, 20))

        self.text_box = ctk.CTkTextbox(
            self.root,
            width=500,
            height=300,
            font=("Consolas", 14)
        )
        self.text_box.pack(pady=10, padx=20)

        save_btn = ctk.CTkButton(
            self.root,
            text="💾 Save File",
            width=150,
            fg_color="#10B981",
            hover_color="#059669",
            command=self.save_current_file
        )
        save_btn.pack(pady=20)

    def save_current_file(self):
        content = self.text_box.get("1.0", "end-1c")
        if not content.strip():
            messagebox.showerror("Error", "⚠️ File cannot be empty!")
            return

        filename = simpledialog.askstring("Save As", "Enter file name (without extension):")
        if not filename:
            return
        
        filename = f"{filename}.txt"
        
        try:
            user_dir = os.path.join(VAULT_DIR, self.current_user)
            os.makedirs(user_dir, exist_ok=True)
            
            encrypted_content = self.encrypt_content(content)
            hashed_filename = self.hash_filename(filename)
            
            with open(os.path.join(user_dir, hashed_filename), "wb") as f:
                f.write(encrypted_content)
            
            self.update_filename_mapping(filename, hashed_filename)
            
            messagebox.showinfo("Success", f"✅ File saved securely!")
            self.open_vault()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")

    def update_filename_mapping(self, original_name, hashed_name):
        mapping_path = os.path.join(VAULT_DIR, self.current_user, ".filenames.json")
        
        try:
            if os.path.exists(mapping_path):
                with open(mapping_path, "r") as f:
                    mappings = json.load(f)
            else:
                mappings = {}
                
            mappings[hashed_name] = original_name
            
            with open(mapping_path, "w") as f:
                json.dump(mappings, f, indent=4)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not update filename mapping:\n{e}")

    def get_original_filenames(self):
        mapping_path = os.path.join(VAULT_DIR, self.current_user, ".filenames.json")
        if os.path.exists(mapping_path):
            with open(mapping_path, "r") as f:
                return json.load(f)
        return {}

    def upload_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file to upload",
            filetypes=[("All Files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            user_dir = os.path.join(VAULT_DIR, self.current_user)
            os.makedirs(user_dir, exist_ok=True)
            
            original_filename = os.path.basename(filepath)
            
            # Check if filename exists in mappings (not filesystem)
            mappings = self.get_original_filenames()
            if original_filename in mappings.values():
                if not messagebox.askyesno("File Exists", f"'{original_filename}' already exists. Overwrite?"):
                    return
            
            # Read and encrypt file content
            with open(filepath, 'rb') as f:
                file_content = f.read()
            
            encrypted_content = self.encrypt_content(file_content)
            hashed_filename = self.hash_filename(original_filename)
            
            # Save encrypted file
            with open(os.path.join(user_dir, hashed_filename), 'wb') as f:
                f.write(encrypted_content)
            
            # Update filename mapping
            self.update_filename_mapping(original_filename, hashed_filename)
            
            messagebox.showinfo("Success", f"✅ File uploaded and secured: {original_filename}")
            
        except Exception as e:
            messagebox.showerror("Upload Failed", f"Could not upload file:\n{e}")

    def show_saved_files(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        back_btn = ctk.CTkButton(
            self.root,
            text="← Back to Vault",
            width=120,
            fg_color="#6B7280",
            hover_color="#4B5563",
            font=("Segoe UI", 12),
            command=self.open_vault
        )
        back_btn.place(x=20, y=20)

        heading = ctk.CTkLabel(
            self.root,
            text="📂 Your Saved Files",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        heading.pack(pady=(60, 20))

        files_frame = ctk.CTkFrame(self.root)
        files_frame.pack(pady=10, padx=20, fill="both", expand=True)

        mappings = self.get_original_filenames()
        if not mappings:
            no_files_label = ctk.CTkLabel(
                files_frame,
                text="No files found. Create your first file!",
                font=("Segoe UI", 14)
            )
            no_files_label.pack(pady=50)
            return

        scrollable_frame = ctk.CTkScrollableFrame(
            files_frame,
            width=500,
            height=300
        )
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for original_name in mappings.values():
            file_frame = ctk.CTkFrame(scrollable_frame)
            file_frame.pack(pady=5, padx=5, fill="x")

            file_label = ctk.CTkLabel(
                file_frame,
                text=original_name,
                font=("Consolas", 12),
                anchor="w"
            )
            file_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            view_btn = ctk.CTkButton(
                file_frame,
                text="View",
                width=60,
                fg_color="#3B82F6",
                hover_color="#1D4ED8",
                command=lambda f=original_name: self.view_file(f)
            )
            view_btn.pack(side="right", padx=5)

            delete_btn = ctk.CTkButton(
                file_frame,
                text="Delete",
                width=60,
                fg_color="#EF4444",
                hover_color="#B91C1C",
                command=lambda f=original_name: self.delete_file(f)
            )
            delete_btn.pack(side="right", padx=5)

    def view_file(self, filename):
        try:
            mappings = self.get_original_filenames()
            hashed_name = next(k for k,v in mappings.items() if v == filename)
            
            file_path = os.path.join(VAULT_DIR, self.current_user, hashed_name)
            
            with open(file_path, "rb") as f:
                encrypted_content = f.read()
            
            content = self.decrypt_content(encrypted_content)
            
            view_window = ctk.CTkToplevel(self.root)
            view_window.title(f"Viewing: {filename}")
            view_window.geometry("600x500")
            view_window.attributes('-topmost', True)
            view_window.focus_force()
            view_window.after(100, lambda: view_window.attributes('-topmost', False))
            
            back_btn = ctk.CTkButton(
                view_window,
                text="← Close",
                width=80,
                fg_color="#6B7280",
                hover_color="#4B5563",
                font=("Segoe UI", 12),
                command=view_window.destroy
            )
            back_btn.pack(pady=10, padx=10, anchor="nw")
            
            content_text = ctk.CTkTextbox(
                view_window,
                width=550,
                height=400,
                font=("Consolas", 12),
                wrap="word"
            )
            content_text.pack(pady=10, padx=10, fill="both", expand=True)
            content_text.insert("1.0", content)
            content_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def delete_file(self, filename):
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {filename}?"):
            return
        
        try:
            mappings = self.get_original_filenames()
            hashed_name = next(k for k,v in mappings.items() if v == filename)
            
            file_path = os.path.join(VAULT_DIR, self.current_user, hashed_name)
            os.remove(file_path)
            
            # Update mappings
            del mappings[hashed_name]
            mapping_path = os.path.join(VAULT_DIR, self.current_user, ".filenames.json")
            with open(mapping_path, "w") as f:
                json.dump(mappings, f, indent=4)
            
            messagebox.showinfo("Success", f"Deleted: {filename}")
            self.show_saved_files()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete file:\n{e}")

    def open_vault(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        heading = ctk.CTkLabel(self.root, text=f"🔐 Welcome, {self.current_user}", 
                            font=("Segoe UI", 20, "bold"))
        heading.pack(pady=30)

        create_btn = ctk.CTkButton(self.root, text="📝 Write and Save Text File", 
                                command=self.open_text_editor)
        create_btn.pack(pady=10)

        upload_btn = ctk.CTkButton(self.root, text="📁 Upload File from PC", 
                                command=self.upload_file)
        upload_btn.pack(pady=10)

        show_btn = ctk.CTkButton(self.root, text="📂 Show My Saved Files", 
                                command=self.show_saved_files)
        show_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self.root, text="⬅️ Logout", command=self.create_widgets)
        back_btn.pack(pady=30)

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.root,
            text="🔐 Your Personal File Locker",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#2b2b2b")
        title.pack(pady=50)

        login_btn = ctk.CTkButton(self.root, text="Login", width=220, height=45, font=("Segoe UI", 15),
                                fg_color="#3B82F6", hover_color="#1D4ED8", text_color="white",
                                command=self.open_login)
        login_btn.pack(pady=15)

        signup_btn = ctk.CTkButton(self.root, text="Sign Up", width=220, height=45, font=("Segoe UI", 15),
                                 fg_color="#10B981", hover_color="#059669", text_color="white",
                                 command=self.open_signup)
        signup_btn.pack(pady=15)

        exit_btn = ctk.CTkButton(self.root, text="Exit", width=160, height=40, font=("Segoe UI", 13),
                               fg_color="#EF4444", hover_color="#B91C1C", text_color="white",
                               command=self.confirm_exit)
        exit_btn.pack(pady=30)

    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainPage(root)
    root.mainloop()