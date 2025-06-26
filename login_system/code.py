import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

def login():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x350")
    login_window.configure(bg="#e6f2ff")

    tk.Label(login_window, text="Login to Your Account", font=("Helvetica", 16, "bold"), 
             bg="#e6f2ff", fg="#003366").pack(pady=20)

    # Initialize 'users' first to avoid UnboundLocalError
    users = {}  # <-- FIX: Define 'users' upfront

    try:
        if os.path.exists("users.json"):
            if os.path.getsize("users.json") > 0:  # Check file size separately
                with open("users.json", "r") as file:
                    users = json.load(file)
    except json.JSONDecodeError:
        messagebox.showwarning("Warning", "User data file is corrupted. Starting fresh.")
        users = {}  # Reset to empty dict
    except Exception as e:  # Catch ALL other errors
        messagebox.showerror("Error", f"Failed to load users: {str(e)}")
        login_window.destroy()
        return

    # Now 'users' is always defined, even if an error occurred
    if not users:
        messagebox.showinfo("Info", "No users registered yet!")
        login_window.destroy()
        return

    tk.Label(login_window, text="Select Username:", bg="#e6f2ff").pack(pady=5)
    
    # Create a combobox with existing usernames
    username_var = tk.StringVar()
    username_combobox = ttk.Combobox(login_window, textvariable=username_var, width=27)
    username_combobox['values'] = list(users.keys())
    username_combobox.pack()
    
    # Initially hide password widgets
    password_label = tk.Label(login_window, text="Enter Password:", bg="#e6f2ff")
    password_entry = tk.Entry(login_window, show="*", width=30)
    
    def on_username_select(event):
        # Show password entry when username is selected
        password_label.pack(pady=5)
        password_entry.pack()
        login_button.pack(pady=20)
    
    username_combobox.bind("<<ComboboxSelected>>", on_username_select)

    def verify_login():
        username = username_var.get()
        password = password_entry.get()
        
        if username not in users:
            messagebox.showerror("Error", "Username not found!")
            return
            
        if users[username]["password"] == password:
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            open_study_planner(username)
        else:
            messagebox.showerror("Error", "Incorrect password!")
    
    login_button = tk.Button(login_window, text="Login", command=verify_login, bg="#4CAF50", fg="white", width=20, height=2)
    
    # Initially pack only the username selection
    username_combobox.pack(pady=10)

def open_study_planner(username):
    planner_window = tk.Toplevel(root)
    planner_window.title(f"Study Planner - {username}")
    planner_window.geometry("800x600")
    planner_window.configure(bg="#f0f8ff")
    
    # Load user data
    with open("users.json", "r") as file:
        users = json.load(file)
    user_data = users.get(username, {"subjects": {}})
    
    tk.Label(planner_window, text=f"📚 {username}'s Study Planner", font=("Helvetica", 18, "bold"), 
             bg="#f0f8ff", fg="#003366").pack(pady=20)
    
    if not user_data["subjects"]:
        tk.Label(planner_window, text="No subjects added yet!", font=("Helvetica", 14), 
                 bg="#f0f8ff").pack(pady=50)
    else:
        # Display subjects if they exist
        tk.Label(planner_window, text="Your Subjects:", font=("Helvetica", 14), 
                 bg="#f0f8ff").pack(pady=10)
        for subject in user_data["subjects"]:
            tk.Label(planner_window, text=f"- {subject}", font=("Helvetica", 12), 
                     bg="#f0f8ff").pack()

def save_user(username, password):
    data = {}
    
    try:
        # Try to load existing data if file exists and is not empty
        if os.path.exists("users.json") and os.path.getsize("users.json") > 0:
            with open("users.json", "r") as file:
                data = json.load(file)
    except json.JSONDecodeError:
        # If file contains invalid JSON, start with empty data
        data = {}
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read user data: {str(e)}")
        return

    # Check if username already exists
    if username in data:
        messagebox.showerror("Error", "Username already exists!")
        return

    # Add new user
    data[username] = {
        "password": password,
        "subjects": {}
    }

    try:
        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo("Success", "User registered successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save user: {str(e)}")

def open_signup():
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("400x350")
    signup_window.configure(bg="#e6f2ff")

    tk.Label(signup_window, text="Create New Account", font=("Helvetica", 16, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=20)

    tk.Label(signup_window, text="Enter Username:", bg="#e6f2ff").pack(pady=5)
    username_entry = tk.Entry(signup_window, width=30)
    username_entry.pack()

    tk.Label(signup_window, text="Set Password:", bg="#e6f2ff").pack(pady=5)
    password_entry = tk.Entry(signup_window, show="*", width=30)
    password_entry.pack()

    tk.Label(signup_window, text="Confirm Password:", bg="#e6f2ff").pack(pady=5)
    confirm_entry = tk.Entry(signup_window, show="*", width=30)
    confirm_entry.pack()

    def submit_signup():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        confirm_password = confirm_entry.get().strip()

        if username == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        save_user(username, password)
        signup_window.destroy()

    tk.Button(signup_window, text="Sign Up", command=submit_signup, bg="#4CAF50", fg="white", width=20, height=2).pack(pady=20)

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("📘 Student Study Planner")
root.geometry("600x400")
root.configure(bg="#f0f8ff")

welcome_label = tk.Label(
    root,
    text="🎓 Welcome to Student Study Planner!",
    font=("Helvetica", 22, "bold"),
    bg="#f0f8ff",
    fg="#003366"
)
welcome_label.pack(pady=40)

login_button = tk.Button(root, text="🔐 Already have an account? Login", command=login, 
                        font=("Arial", 14), bg="#4CAF50", fg="white", width=30, height=2)
login_button.pack(pady=15)

signup_button = tk.Button(root, text="🆕 New here? Sign Up", command=open_signup, 
                         font=("Arial", 14), bg="#4CAF50", fg="white", width=30, height=2)
signup_button.pack(pady=10)

root.mainloop()