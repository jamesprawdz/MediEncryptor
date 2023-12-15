from cryptography.fernet import Fernet
import os

# Load the encryption key from environment variable
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")

# Encrypt data using AES
def encrypt_data(plaintext):
    fernet = Fernet(ENCRYPTION_KEY)
    encrypted_data = fernet.encrypt(plaintext.encode())
    return encrypted_data

# Decrypt data using AES
def decrypt_data(ciphertext):
    fernet = Fernet(ENCRYPTION_KEY)
    decrypted_data = fernet.decrypt(ciphertext).decode()
    return decrypted_data
