# 🔐 EncryptedFileVault

A secure, GUI-based file encryption vault built using Python and Tkinter. Users can **sign up**, **log in**, **encrypt/decrypt files**, and safely store them using strong encryption techniques.

---

## 🚀 Features

- 👤 User Signup and Login system
- 🔒 AES-based File Encryption and Decryption
- 📁 Secure File Vault to manage encrypted files
- 🧠 User-friendly GUI built with Tkinter
- 🧰 Modular structure for easy understanding and extensibility

---

## 🛠️ Tech Stack & Modules Used

| Technology / Library | Purpose |
|----------------------|---------|
| **Python**           | Core programming language |
| **Tkinter**          | GUI interface for all windows |
| **os, shutil**       | File system operations |
| **hashlib**          | Password hashing (SHA-256) |
| **cryptography.fernet** | Symmetric AES encryption and decryption |
| **json**             | User data and vault metadata storage |

---


---

## 🔧 How It Works

1. **Signup (`signup.py`)**
   - New users register with a username and password.
   - Passwords are hashed and stored securely.

2. **Login (`login.py`)**
   - Validates user credentials using stored hash.

3. **Vault (`vault.py`)**
   - After login, users can add files.
   - Files are encrypted using Fernet (AES).
   - Encrypted files are stored in a local vault folder.

4. **Encryption (`encryption.py`)**
   - Encrypts files before storing.
   - Decrypts files when needed, only with the correct key.

5. **Main App (`app.py`)**
   - Connects all modules.
   - Acts as an entry point for launching the app.

---

## 🧪 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/encryption.git
cd encryption/EncryptedFileVault


