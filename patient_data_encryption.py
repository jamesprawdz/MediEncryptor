from cryptography.fernet import Fernet
from encryption_config import ENCRYPTION_KEY  # Import the encryption key


# Encrypt data using AES
def encrypt_data(key, plaintext):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(plaintext.encode())
    return encrypted_data


# Decrypt data using AES
def decrypt_data(key, ciphertext):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(ciphertext).decode()
    return decrypted_data
