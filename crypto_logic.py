import os
from argon2 import low_level
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# This turns your Master Password into a high-security key
def derive_key(master_password: str, salt: bytes) -> bytes:
    return low_level.hash_secret_raw(
        secret=master_password.encode(),
        salt=salt,
        time_cost=3,        # How many times to run the algorithm
        memory_cost=65536,  # Uses 64MB of RAM to slow down hackers
        parallelism=4,      # Number of CPU cores to use
        hash_len=32,        # We need exactly 32 bytes for AES-256
        type=low_level.Type.ID
    )

def encrypt_data(plain_text: str, master_password: str):
    # Salt: Unique per entry to prevent 'rainbow table' attacks
    salt = os.urandom(16)
    # Nonce: 'Number used once'. Critical for AES-GCM security
    nonce = os.urandom(12)
    
    # Generate the key using our Master Password
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    
    # Scramble the data!
    ciphertext = aesgcm.encrypt(nonce, plain_text.encode(), None)
    
    return {"salt": salt, "nonce": nonce, "ciphertext": ciphertext}

def decrypt_data(package, master_password: str):
    try:
        key = derive_key(master_password, package["salt"])
        aesgcm = AESGCM(key)
        
        # Unscramble the data
        decrypted = aesgcm.decrypt(package["nonce"], package["ciphertext"], None)
        return decrypted.decode()
    except Exception:
        return None # Return None if password was wrong