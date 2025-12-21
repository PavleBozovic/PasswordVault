import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import secrets
import string
import ctypes
import win32clipboard
from crypto_logic import encrypt_data, decrypt_data
from database import init_db, add_entry, delete_entry

class AddEntryWindow:
    def __init__(self, parent, master_pass, refresh_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Add New Credential")
        self.top.geometry("350x300")
        self.master_pass = master_pass
        self.refresh_callback = refresh_callback 

        tk.Label(self.top, text="Service Name:").pack(pady=2)
        self.service_input = tk.Entry(self.top, width=30)
        self.service_input.pack(pady=5)

        tk.Label(self.top, text="Password:").pack(pady=2)
        self.pass_input = tk.Entry(self.top, show="*", width=30)
        self.pass_input.pack(pady=5)

        tk.Button(self.top, text="Generate Strong Password", command=self.generate_suggested).pack(pady=5)

        tk.Button(self.top, text="Save Encrypted", command=self.handle_save, bg="#4CAF50", fg="white").pack(pady=20)

    def generate_suggested(self):
        """Creates a random 16-character password and fills the box."""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for i in range(16))
        self.pass_input.delete(0, tk.END)
        self.pass_input.insert(0, password)

    def handle_save(self):
        srv = self.service_input.get()
        pwd = self.pass_input.get()

        if srv and pwd:
            encrypted = encrypt_data(pwd, self.master_pass)

            print(f"DEBUG: Scrambling '{srv}' password...")
            print(f"DEBUG: Saving encrypted data -> {encrypted['ciphertext'].hex()}")
            
            add_entry(srv, "my_user", encrypted)
            messagebox.showinfo("Success", f"Saved {srv}!")
            self.refresh_callback() 
            self.top.destroy()
        else:
            messagebox.showwarning("Error", "Please fill all fields")

class VaultDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Secure Vault")
        self.root.geometry("700x500")
        self.master_pass = "temp_password" 
        
        init_db() 
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="My Secure Passwords", font=("Arial", 18, "bold")).pack(pady=15)

        self.tree = ttk.Treeview(self.root, columns=("Service", "User"), show='headings')
        self.tree.heading("Service", text="Service / Website")
        self.tree.heading("User", text="Username")
        self.tree.pack(fill="both", expand=True, padx=20)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=25)

        tk.Button(btn_frame, text="+ Add New", command=self.open_add_window, width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="📋 Copy Pass", command=self.copy_password, width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="🗑️ Delete", command=self.handle_delete, width=15, fg="red").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="🔄 Refresh", command=self.load_data, width=15).grid(row=0, column=3, padx=5)

        self.load_data() 

    def open_add_window(self):
        AddEntryWindow(self.root, self.master_pass, self.load_data)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect("vault.db")
        cursor = conn.cursor()
        cursor.execute("SELECT service, username FROM credentials")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def copy_password(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select an entry first")
            return

        service_name = self.tree.item(selected)['values'][0]

        conn = sqlite3.connect("vault.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ciphertext, nonce, salt FROM credentials WHERE service=?", (service_name,))
        row = cursor.fetchone()
        conn.close()

        if row:
            package = {"ciphertext": row[0], "nonce": row[1], "salt": row[2]}
            raw_password = decrypt_data(package, self.master_pass)
            
            if raw_password:
                self.root.clipboard_clear()
                self.root.clipboard_append(raw_password)
                messagebox.showinfo("Copied", f"Password for {service_name} is now in clipboard.")  

                self.root.after(30000, self.secure_clear_clipboard)
                
    def secure_clear_clipboard(self):
        """Advanced clear to bypass Windows Clipboard History ($Win + V)"""
        try:
            self.root.clipboard_clear()
        
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
            
            ctypes.windll.user32.OpenClipboard(None)
            ctypes.windll.user32.EmptyClipboard()
            ctypes.windll.user32.CloseClipboard()
            
            print("DEBUG: Clipboard and History wiped.")
        except Exception as e:
            print(f"DEBUG: Secure wipe failed: {e}")

    def handle_delete(self):
        """Fetches the selected name and calls the database delete function."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select an entry to delete")
            return

        service_name = self.tree.item(selected)['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete credentials for {service_name}?"):
            delete_entry(service_name)
            self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = VaultDashboard(root)
    root.mainloop()