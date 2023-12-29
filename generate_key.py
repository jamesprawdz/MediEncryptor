import os


def generate_encryption_key():
    # 32 bytes = 256 bits
    key = os.urandom(32)  # Generate a 256-bit random key
    return key


if __name__ == "__main__":
    key = generate_encryption_key()
    print("Generated Encryption Key:", key.hex())
