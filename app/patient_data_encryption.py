from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import binascii  # Import binascii for hex conversion

# Ensure this is 32 bytes (256 bits) for AES-256
hex_key = os.environ.get("ENCRYPTION_KEY")  # This will be a hex string
if hex_key is None:
    raise ValueError("No ENCRYPTION_KEY found in environment variables")
ENCRYPTION_KEY = binascii.unhexlify(hex_key)  # Convert hex to bytes


def encrypt_data(plaintext):
    padder = padding.PKCS7(128).padder()  # AES block size is 128 bits
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    iv = os.urandom(16)  # AES block size is 16 bytes
    # print("Generated IV:", iv.hex())  # Print the IV in hexadecimal format for readability

    cipher = Cipher(
        algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ct  # Prepend the IV for use in decryption


def decrypt_data(ciphertext):
    iv = ciphertext[:16]  # Extract the IV from the start
    ct = ciphertext[16:]  # The rest is the actual ciphertext
    cipher = Cipher(
        algorithms.AES(ENCRYPTION_KEY), modes.CBC(iv), backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ct) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()  # AES block size is 128 bits
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data.decode(
        "utf-8"
    )  # Decode from bytes to string after decryption
