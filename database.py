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

def delete_entry(entry_id):
    """Removes a specific credential row by its ID."""
    with sqlite3.connect("vault.db") as conn:
        cursor = conn.cursor()
        # We use the 'id' because it's unique and safer than deleting by name
        cursor.execute("DELETE FROM credentials WHERE id = ?", (entry_id,))
        conn.commit()
        print(f"Entry {entry_id} deleted successfully.")    
    