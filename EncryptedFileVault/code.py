import customtkinter as ctk
from tkinter import messagebox, simpledialog
import hashlib
import smtplib
import json
import os
import random
from tkinter import filedialog
import re

# === File Path Setup ===
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
USERDATA_PATH = os.path.join(PROJECT_DIR, "userdata.json")

# === Theme Setup ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

# === Helper Functions ===
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_otp_to_email(email):
    otp = str(random.randint(100000, 999999))
    sender_email = "iamshreyabhat@gmail.com"
    sender_pass = "vxprnzeaytakuqmb"
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
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def load_user_data():
    try:
        if os.path.exists(USERDATA_PATH):
            with open(USERDATA_PATH, "r") as f:
                data = json.load(f)
                if not isinstance(data, dict):  # Check if data is a dictionary
                    return {}
                return data
        return {}
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return {}

class MainPage:
    def __init__(self, root):
        self.root = root
        self.current_user = None  # Add this to store logged-in user
        self.current_password = None  # Add this if needed for encryption later
        self.root.title("Secure File Vault")
        self.root.geometry("600x500")
        self.root.configure(bg="#dce3f0")
        self.root.resizable(False, False)
        self.create_widgets()
    
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

        username_label = ctk.CTkLabel(self.root, text="Username:", font=("Segoe UI", 13))
        username_label.pack(pady=(10, 2))
        username_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter username")
        username_entry.pack(pady=5)

        email_label = ctk.CTkLabel(self.root, text="Email:", font=("Segoe UI", 13))
        email_label.pack(pady=(10, 2))
        email_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter email")
        email_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self.root, text="Password:", font=("Segoe UI", 13))
        password_label.pack(pady=(10, 2))
        password_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter password", show="*")
        password_entry.pack(pady=5)

        confirm_label = ctk.CTkLabel(self.root, text="Confirm Password:", font=("Segoe UI", 13))
        confirm_label.pack(pady=(10, 2))
        confirm_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Re-enter password", show="*")
        confirm_entry.pack(pady=5)

        def submit_signup():
            uname = username_entry.get().strip()
            email = email_entry.get().strip().lower()
            pwd = password_entry.get().strip()
            confirm_pwd = confirm_entry.get().strip()

            if not uname or not email or not pwd or not confirm_pwd:
                messagebox.showerror("Error", "⚠️ Please fill all fields.")
                return

            if pwd != confirm_pwd:
                messagebox.showerror("Mismatch", "Passwords do not match.")
                return

            if not is_valid_email(email):
                messagebox.showerror("Invalid Email", "Please enter a valid email address.")
                return

            users = load_user_data()

            for user, data in users.items():
                if user == uname:
                    messagebox.showerror("Duplicate", "Username already exists.")
                    return
                if data["email"] == email:
                    messagebox.showerror("Duplicate", "Email already registered.")
                    return

            otp_sent = send_otp_to_email(email)
            if not otp_sent:
                return

            otp_entered = simpledialog.askstring("OTP Verification", "Enter the OTP sent to your email:")
            if otp_entered is None or otp_entered != otp_sent:
                messagebox.showerror("Incorrect OTP", "OTP did not match. Signup failed.")
                return

            hashed_pwd = hash_password(pwd)
            users[uname] = {
                "email": email,
                "password": hashed_pwd
            }

            try:
                with open(USERDATA_PATH, "w") as f:
                    json.dump(users, f, indent=4)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save user data: {e}")
                return

            messagebox.showinfo("Success", f"Account created successfully for {uname}!")
            self.current_user = uname  
            self.current_password = pwd  
            self.open_vault()

        submit_btn = ctk.CTkButton(self.root, text="Submit", width=150, fg_color="#10B981",
                                   hover_color="#059669", command=submit_signup)
        submit_btn.pack(pady=20)

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

        email_label = ctk.CTkLabel(self.root, text="Email:", font=("Segoe UI", 13))
        email_label.pack(pady=(10, 2))
        email_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter your email")
        email_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self.root, text="Password:", font=("Segoe UI", 13))
        password_label.pack(pady=(10, 2))
        password_entry = ctk.CTkEntry(self.root, width=250, placeholder_text="Enter password", show="*")
        password_entry.pack(pady=5)

        def perform_login():
            email = email_entry.get().strip().lower()
            pwd = password_entry.get().strip()

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
                        messagebox.showinfo("Success", f"✅ Logged in as {uname}")
                        self.open_vault()
                        return
                    else:
                        messagebox.showerror("Error", "❌ Incorrect password.")
                        return

            messagebox.showerror("Error", "❌ Email not registered.")

        login_btn = ctk.CTkButton(self.root, text="Login", width=150,
                                  fg_color="#3B82F6", hover_color="#1D4ED8",
                                  command=perform_login)
        login_btn.pack(pady=20)

        forgot_btn = ctk.CTkButton(self.root, text="Forgot Password?", width=180,
                                   fg_color="#9CA3AF", hover_color="#6B7280",
                                   command=self.reset)
        forgot_btn.pack(pady=10)
    

    def open_text_editor(self):
        # Clear the vault screen completely
        for widget in self.root.winfo_children():
            widget.destroy()

        # Back button (top-left)
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

        # Heading
        heading = ctk.CTkLabel(
            self.root,
            text="✍️ Write Your File",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        heading.pack(pady=(60, 20))

        # Text box (bigger)
        self.text_box = ctk.CTkTextbox(
            self.root,
            width=500,
            height=300,
            font=("Consolas", 14)
        )
        self.text_box.pack(pady=10, padx=20)

        # Save button (bottom)
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
            return  # User cancelled

        # Create user's vault directory
        user_dir = os.path.join(PROJECT_DIR, "vault", self.current_user)
        os.makedirs(user_dir, exist_ok=True)

        # Save as .txt file
        try:
            with open(os.path.join(user_dir, f"{filename}.txt"), "w") as f:
                f.write(content)
            messagebox.showinfo("Success", f"✅ Saved as: {filename}.txt")
            self.open_vault()  # Return to vault
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save:\n{e}")

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
                                command=self.show_saved_files)  # Updated to call show_saved_files
        show_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self.root, text="⬅️ Logout", command=self.create_widgets)
        back_btn.pack(pady=30)


    def upload_file(self):
        # Open file dialog to select a file
        filepath = filedialog.askopenfilename(
            title="Select a file to upload",
            filetypes=[("All Files", "*.*")]
        )
        
        if not filepath:  # User cancelled
            return
        
        try:
            # Create user's vault directory if it doesn't exist
            user_dir = os.path.join(PROJECT_DIR, "vault", self.current_user)
            os.makedirs(user_dir, exist_ok=True)
            
            # Get just the filename (without path)
            filename = os.path.basename(filepath)
            dest_path = os.path.join(user_dir, filename)
            
            # Check if file already exists
            if os.path.exists(dest_path):
                if not messagebox.askyesno("File Exists", f"'{filename}' already exists. Overwrite?"):
                    return
            
            # Copy the file
            with open(filepath, 'rb') as src_file:
                with open(dest_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())
            
            messagebox.showinfo("Success", f"Uploaded: {filename}")
            
        except Exception as e:
            messagebox.showerror("Upload Failed", f"Could not upload file:\n{e}")

        
    def show_saved_files(self):
        # Clear the current screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add back button
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

        # Heading
        heading = ctk.CTkLabel(
            self.root,
            text="📂 Your Saved Files",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        heading.pack(pady=(60, 20))

        # Create frame to hold the files list
        files_frame = ctk.CTkFrame(self.root)
        files_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Get the user's vault directory
        user_dir = os.path.join(PROJECT_DIR, "vault", self.current_user)
        
        # Check if directory exists and has files
        if not os.path.exists(user_dir):
            no_files_label = ctk.CTkLabel(
                files_frame,
                text="No files found. Create your first file!",
                font=("Segoe UI", 14)
            )
            no_files_label.pack(pady=50)
            return
        
        files = os.listdir(user_dir)
        if not files:
            no_files_label = ctk.CTkLabel(
                files_frame,
                text="No files found. Create your first file!",
                font=("Segoe UI", 14)
            )
            no_files_label.pack(pady=50)
            return

        # Create scrollable frame for files
        scrollable_frame = ctk.CTkScrollableFrame(
            files_frame,
            width=500,
            height=300
        )
        scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Display each file with options
        for filename in files:
            file_frame = ctk.CTkFrame(scrollable_frame)
            file_frame.pack(pady=5, padx=5, fill="x")

            # File name label
            file_label = ctk.CTkLabel(
                file_frame,
                text=filename,
                font=("Consolas", 12),
                anchor="w"
            )
            file_label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

            # View button
            view_btn = ctk.CTkButton(
                file_frame,
                text="View",
                width=60,
                fg_color="#3B82F6",
                hover_color="#1D4ED8",
                command=lambda f=filename: self.view_file(f)
            )
            view_btn.pack(side="right", padx=5)

            # Delete button
            delete_btn = ctk.CTkButton(
                file_frame,
                text="Delete",
                width=60,
                fg_color="#EF4444",
                hover_color="#B91C1C",
                command=lambda f=filename: self.delete_file(f)
            )
            delete_btn.pack(side="right", padx=5)

    def view_file(self, filename):
        # Get the full file path
        file_path = os.path.join(PROJECT_DIR, "vault", self.current_user, filename)
        
        try:
            with open(file_path, "r") as f:
                content = f.read()
            
            # Create a new window to display the file
            view_window = ctk.CTkToplevel(self.root)
            view_window.title(f"Viewing: {filename}")
            view_window.geometry("600x500")
            view_window.resizable(True, True)
            
            # Make the window stay on top
            view_window.attributes('-topmost', True)  # This line keeps it on top
            view_window.focus_force()  # This gives it focus
            
            # After it's shown, we can set it to behave normally
            view_window.after(100, lambda: view_window.attributes('-topmost', False))
            
            # Back button
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
            
            # File content display
            content_text = ctk.CTkTextbox(
                view_window,
                width=550,
                height=400,
                font=("Consolas", 12),
                wrap="word"
            )
            content_text.pack(pady=10, padx=10, fill="both", expand=True)
            content_text.insert("1.0", content)
            content_text.configure(state="disabled")  # Make it read-only
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def delete_file(self, filename):
        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {filename}?"):
            return
        
        # Get the full file path
        file_path = os.path.join(PROJECT_DIR, "vault", self.current_user, filename)
        
        try:
            os.remove(file_path)
            messagebox.showinfo("Success", f"Deleted: {filename}")
            self.show_saved_files()  # Refresh the file list
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete file:\n{e}")

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