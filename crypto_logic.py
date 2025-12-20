import os
from argon2 import low_level, PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ph = PasswordHasher(
    time_cost=3, 
    memory_cost=65536, 
    parallelism=4
)

def hash_master_password(password: str) -> str:
    """Hashes the master password for storage during first-time setup."""
    return ph.hash(password)

def verify_master_password(stored_hash: str, provided_password: str) -> bool:
    """Checks if the entered password matches the stored Argon2 hash."""
    try:
        return ph.verify(stored_hash, provided_password)
    except Exception:
        return False

def derive_key(master_password: str, salt: bytes) -> bytes:
    """Turns the Master Password into a high-security 32-byte key."""
    return low_level.hash_secret_raw(
        secret=master_password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=low_level.Type.ID
    )

def encrypt_data(plain_text: str, master_password: str):
    """Scrambles data into a ciphertext package."""
    salt = os.urandom(16)
    nonce = os.urandom(12)
    
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    
    ciphertext = aesgcm.encrypt(nonce, plain_text.encode(), None)
    
    del key 
    
    return {"salt": salt, "nonce": nonce, "ciphertext": ciphertext}

def decrypt_data(package, master_password: str):
    """Unscrambles the ciphertext package back to plain text."""
    try:
        key = derive_key(master_password, package["salt"])
        aesgcm = AESGCM(key)
        
        decrypted = aesgcm.decrypt(package["nonce"], package["ciphertext"], None)
        
        del key
        return decrypted.decode()
    except Exception as e:
        return None