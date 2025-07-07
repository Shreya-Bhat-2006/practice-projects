import tkinter as tk
import tkinter.messagebox as msg
import tkinter.simpledialog
import json
import os
import hashlib
from tkinter.ttk import Combobox
import smtplib
import random
from cryptography.fernet import Fernet

class AuthApp:
    def load_or_create_key(self):
        key_file = "secret.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def __init__(self):
        self.fernet = Fernet(self.load_or_create_key())
        self.window = tk.Tk()
        self.window.title("Secure Notepad App")
        self.window.geometry("500x400")
        self.window.config(bg="#ffe6f0")
        self.current_user = None
        self.show_welcome_screen()
        self.window.mainloop()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def send_otp_to_email(self, email):
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
            msg.showerror("Email Error", f"❌ Could not send OTP:\n{e}")
            return None

    def show_welcome_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        tk.Label(self.window, text="✨ Welcome to Secure Notepad ✨", font=("Arial", 18, "bold"),
                 bg="#ffe6f0", fg="#800040").pack(pady=30)

        tk.Button(self.window, text="Login", width=20, font=("Arial", 14, "bold"), bg="#ffb3d9",
                  command=self.show_login_screen).pack(pady=10)

        tk.Button(self.window, text="Sign Up", width=20, font=("Arial", 14, "bold"), bg="#d9b3ff",
                  command=self.show_signup_screen).pack(pady=10)

        tk.Button(self.window, text="Exit", width=20, font=("Arial", 14, "bold"), bg="#b3d9ff",
                  command=self.exit_app).pack(pady=10)

    def show_signup_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.config(bg="#f0fff0")

        tk.Label(self.window, text="🔐 Create Account", font=("Arial", 18, "bold"), bg="#f0fff0", fg="#006600").pack(pady=20)

        self.name_entry = tk.Entry(self.window, width=30)
        self.email_entry = tk.Entry(self.window, width=30)
        self.pass_entry = tk.Entry(self.window, show="*", width=30)
        self.confirm_entry = tk.Entry(self.window, show="*", width=30)

        for text, widget in zip(["Username:", "Email:", "Password:", "Confirm Password:"],
                                [self.name_entry, self.email_entry, self.pass_entry, self.confirm_entry]):
            tk.Label(self.window, text=text, font=("Arial", 12), bg="#f0fff0").pack()
            widget.pack(pady=5)

        tk.Button(self.window, text="Register", width=20, font=("Arial", 12, "bold"), bg="#ccffcc",
                  command=self.register_clicked).pack(pady=20)

        tk.Button(self.window, text="← Back", width=15, font=("Arial", 12, "bold"), bg="#ccccff",
                  command=self.show_welcome_screen).pack()

    def register_clicked(self):
        name, email = self.name_entry.get().strip(), self.email_entry.get().strip()
        password, confirm = self.pass_entry.get().strip(), self.confirm_entry.get().strip()

        if not name or not email or not password or not confirm:
            msg.showwarning("Input Error", "⚠️ Please fill in all fields.")
            return
        if "@gmail.com" not in email:
            msg.showwarning("Invalid Email", "⚠️ Please enter a valid Gmail address.")
            return
        if password != confirm:
            msg.showwarning("Password Mismatch", "⚠️ Passwords do not match.")
            return

        users = {}
        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as f:
                users = json.load(f)
        if name in users:
            msg.showwarning("User Exists", "⚠️ Username already exists.")
            return
        for details in users.values():
            if details.get("email") == email:
                msg.showwarning("Email Exists", "⚠️ This email is already used.")
                return

        otp = self.send_otp_to_email(email)
        if not otp:
            return

        entered_otp = tk.simpledialog.askstring("OTP Verification", f"📩 Enter OTP sent to {email}:")
        if entered_otp != otp:
            msg.showerror("Invalid OTP", "❌ OTP verification failed.")
            return

        users[name] = {
            "password": self.hash_password(password),
            "email": email
        }
        with open("user_data.json", "w") as f:
            json.dump(users, f, indent=4)

        # Initialize blank note for new user
        notes = {}
        if os.path.exists("notepad_data.json"):
            with open("notepad_data.json", "r") as f:
                notes = json.load(f)
        notes[name] = ""
        with open("notepad_data.json", "w") as f:
            json.dump(notes, f, indent=4)

        self.current_user = name
        self.show_notepad()

    def show_login_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.config(bg="#fff5e6")

        tk.Label(self.window, text="🔐 Login", font=("Arial", 18, "bold"), bg="#fff5e6", fg="#cc6600").pack(pady=20)

        usernames = []
        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as f:
                self.users = json.load(f)
                usernames = list(self.users.keys())

        self.user_combo = Combobox(self.window, values=usernames, state="readonly", width=27)
        self.user_combo.pack(pady=5)

        self.login_pass_entry = tk.Entry(self.window, show="*", width=30)
        tk.Label(self.window, text="Password:", font=("Arial", 12), bg="#fff5e6").pack()
        self.login_pass_entry.pack(pady=5)

        tk.Button(self.window, text="Login", width=20, font=("Arial", 12, "bold"), bg="#ffd699",
                  command=self.check_login).pack(pady=20)
        tk.Button(self.window, text="← Back", width=15, font=("Arial", 12, "bold"), bg="#ccccff",
                  command=self.show_welcome_screen).pack()

    def check_login(self):
        username = self.user_combo.get()
        password = self.login_pass_entry.get().strip()

        if not username or not password:
            msg.showwarning("Input Error", "⚠️ Please enter login details.")
            return

        with open("user_data.json", "r") as f:
            users = json.load(f)

        if username in users and users[username]["password"] == self.hash_password(password):
            self.current_user = username
            self.show_notepad()
        else:
            msg.showerror("Login Failed", "❌ Invalid credentials.")

    def show_notepad(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.config(bg="#e6f7ff")

        # 🔹 Top bar with logout button
        top_frame = tk.Frame(self.window, bg="#e6f7ff")
        top_frame.pack(fill=tk.X, pady=(5, 0), padx=10)
        tk.Button(top_frame, text="⏪ Logout", command=self.show_welcome_screen,
                bg="#ccccff", font=("Arial", 10, "bold")).pack(anchor="ne")

        # 🔹 Title
        tk.Label(self.window, text=f"📝 Notes - {self.current_user}", font=("Arial", 16, "bold"),
                bg="#e6f7ff").pack(pady=10)

        # 🔹 Text area
        self.text_area = tk.Text(self.window, height=15, width=50)
        self.text_area.pack(pady=10)

        # 🔹 Load and decrypt note
        if os.path.exists("notepad_data.json"):
            with open("notepad_data.json", "r") as f:
                notes = json.load(f)
                encrypted_note = notes.get(self.current_user, "")
                try:
                    if encrypted_note:
                        decrypted_note = self.fernet.decrypt(encrypted_note.encode()).decode()
                        self.text_area.insert(tk.END, decrypted_note)
                except Exception as e:
                    msg.showerror("Decryption Error", f"❌ Failed to decrypt notes:\n{e}")

        # 🔹 Save and Delete buttons
        tk.Button(self.window, text="💾 Save", command=self.save_notes, bg="#b3e6b3", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(self.window, text="🗑️ Delete", command=self.delete_notes, bg="#ff9999", font=("Arial", 12, "bold")).pack(pady=5)

    def save_notes(self):
        text = self.text_area.get("1.0", tk.END).strip()
        encrypted_text = self.fernet.encrypt(text.encode()).decode()

        notes = {}
        if os.path.exists("notepad_data.json"):
            with open("notepad_data.json", "r") as f:
                notes = json.load(f)

        notes[self.current_user] = encrypted_text
        with open("notepad_data.json", "w") as f:
            json.dump(notes, f, indent=4)

        msg.showinfo("Saved", "✅ Notes saved securely!")


    def delete_notes(self):
        self.text_area.delete("1.0", tk.END)
        notes = {}
        if os.path.exists("notepad_data.json"):
            with open("notepad_data.json", "r") as f:
                notes = json.load(f)
        notes[self.current_user] = ""
        with open("notepad_data.json", "w") as f:
            json.dump(notes, f, indent=4)
        msg.showinfo("Deleted", "🗑️ Notes deleted.")

    def exit_app(self):
        self.window.destroy()

if __name__ == "__main__":
    AuthApp()
