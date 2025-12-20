import sqlite3

def init_db():
    """Create the table if it doesn't exist yet."""
    with sqlite3.connect("vault.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT,
                username TEXT,
                ciphertext BLOB,
                nonce BLOB,
                salt BLOB
            )
        ''')
        conn.commit()

def add_entry(service, user, encrypted_dict):
    """Saves the encrypted pieces into the database."""
    with sqlite3.connect("vault.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO credentials (service, username, ciphertext, nonce, salt)
            VALUES (?, ?, ?, ?, ?)
        ''', (service, user, encrypted_dict['ciphertext'], 
              encrypted_dict['nonce'], encrypted_dict['salt']))
        conn.commit()

def delete_entry(service_name):
    """Removes a record from the database based on the service name."""
    with sqlite3.connect("vault.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM credentials WHERE service = ?", (service_name,))
        conn.commit()
        print(f"Entry for {service_name} deleted successfully.")

def get_all_entries():
    """Returns all service names and usernames for the dashboard table."""
    with sqlite3.connect("vault.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT service, username FROM credentials")
        return cursor.fetchall()

def get_specific_entry(service_name):
    """Fetches the encrypted parts for a single service."""
    with sqlite3.connect("vault.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ciphertext, nonce, salt FROM credentials WHERE service=?", (service_name,))
        return cursor.fetchone()