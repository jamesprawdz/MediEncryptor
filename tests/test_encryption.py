from dotenv import load_dotenv
import pytest
from app.patient_data_encryption import encrypt_data, decrypt_data
import os

load_dotenv()


ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
# Ensure the encryption key is loaded properly
assert ENCRYPTION_KEY is not None, "ENCRYPTION_KEY must be set in the environment."


# Example test function using pytest
def test_normal_data():
    data = "Patient name: John Doe, Diagnosis: Hypertension, Age: 45"
    assert data == decrypt_data(encrypt_data(data))


def test_empty_string():
    data = ""
    assert data == decrypt_data(encrypt_data(data))


def test_special_non_ascii_characters():
    data = "Patient name: Élise Müller, Diagnosis: 肺炎, Age: 30"
    assert data == decrypt_data(encrypt_data(data))


def test_numeric_data():
    data = "1234567890"
    assert data == decrypt_data(encrypt_data(data))


def test_long_text():
    data = "This is a very long patient record with a lot of information to see how the encryption handles larger amounts of data..."
    assert data == decrypt_data(encrypt_data(data))


def test_short_string():
    data = "Short"
    assert data == decrypt_data(encrypt_data(data))


def test_string_with_only_spaces():
    data = "    "
    assert data == decrypt_data(encrypt_data(data))


def test_string_with_newline_characters():
    data = "\nNewLine\n"
    assert data == decrypt_data(encrypt_data(data))


def test_string_with_special_characters():
    data = "!@#$%^&*()_+-=[]{};':,.<>/?"
    assert data == decrypt_data(encrypt_data(data))
