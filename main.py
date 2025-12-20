import tkinter as tk
from tkinter import messagebox, ttk
# Import the functions we wrote in other files
from crypto_logic import encrypt_data, decrypt_data
from database import init_db, add_entry

class VaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Python Vault")
        self.root.geometry("400x300")
        
        # In a real app, you'd have a login screen. 
        # For now, we ask for the Master Password on start.
        self.master_pass = "temp_password" # In production, get this from a login entry
        
        init_db() # Setup database
        self.create_widgets()

    def create_widgets(self):
        # Basic Add Entry Form
        tk.Label(self.root, text="Service Name:").pack()
        self.service_input = tk.Entry(self.root)
        self.service_input.pack()

        tk.Label(self.root, text="Password to Save:").pack()
        self.pass_input = tk.Entry(self.root, show="*")
        self.pass_input.pack()

        tk.Button(self.root, text="Encrypt & Save", command=self.handle_save).pack(pady=10)

    def handle_save(self):
        srv = self.service_input.get()
        pwd = self.pass_input.get()

        if srv and pwd:
            # 1. Scramble it
            encrypted = encrypt_data(pwd, self.master_pass)
            # 2. Store it
            add_entry(srv, "my_user", encrypted)
            messagebox.showinfo("Success", "Password saved securely!")
        else:
            messagebox.showwarning("Error", "Fill in all fields")

if __name__ == "__main__":
    root = tk.Tk()
    app = VaultApp(root)
    root.mainloop()