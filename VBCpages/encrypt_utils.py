import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pandas as pd
import io

def get_key_from_password(password, salt=None):
    """Generate a Fernet key from a password and salt."""
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def decrypt_to_dataframe(encrypted_data, password, salt):
    """Decrypt encrypted data to a DataFrame using password and salt."""
    try:
        # Generate key from password and salt
        key, _ = get_key_from_password(password, salt)
        
        # Decrypt the data
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Convert back to DataFrame
        return pd.read_csv(io.StringIO(decrypted_data.decode()))
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def decrypt_csv_file(encrypted_path, password):
    """Decrypt a CSV file to a DataFrame."""
    with open(encrypted_path, 'rb') as f:
        salt = f.read(16)  # First 16 bytes are the salt
        encrypted_data = f.read()
    
    return decrypt_to_dataframe(encrypted_data, password, salt)