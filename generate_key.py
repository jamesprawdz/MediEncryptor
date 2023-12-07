from cryptography.fernet import Fernet


def generate_encryption_key():
    key = Fernet.generate_key()
    return key


if __name__ == "__main__":
    key = generate_encryption_key()
    print("Generated Encryption Key:", key.decode())
