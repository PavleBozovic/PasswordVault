# Secure Python Password Vault

A lightweight, high-security desktop application for managing credentials. Built with Python, Tkinter, and industry-standard encryption.

## Features
* **AES-256 GCM Encryption:** Ensures your passwords are mathematically scrambled and tamper-proof.
* **Argon2id Key Derivation:** Protects against brute-force attacks by using a memory-hard hashing function for your Master Password.
* **Local Storage:** Everything is stored in a local SQLite database (`vault.db`). No data ever leaves your machine.
* **Security First:** Includes automatic clipboard clearing (30 seconds) and master password verification.

## Tech Stack
* **Language:** Python 3.x
* **GUI:** Tkinter
* **Database:** SQLite
* **Cryptography:** `cryptography` and `argon2-cffi` libraries.

## Getting Started

### Prerequisites
Ensure you have Python installed. Then, clone the repository and set up your environment:

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/YourUsername/PasswordVault.git](https://github.com/YourUsername/PasswordVault.git)
   cd PasswordVault
