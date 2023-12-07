import unittest
from patient_data_encryption import encrypt_data, decrypt_data
from encryption_config import ENCRYPTION_KEY


class TestEncryptionMethods(unittest.TestCase):
    def test_normal_data(self):
        data = "Patient name: John Doe, Diagnosis: Hypertension, Age: 45"
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_empty_string(self):
        data = ""
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_special_non_ascii_characters(self):
        data = "Patient name: Élise Müller, Diagnosis: 肺炎, Age: 30"
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_numeric_data(self):
        data = "1234567890"
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_long_text(self):
        data = "This is a very long patient record with a lot of information to see how the encryption handles larger amounts of data. It includes various details about the patient's history, medications, diagnosis, treatment plans, and other relevant medical information that might be sensitive and needs to be encrypted securely."
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_short_string(self):
        data = "Short"
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_string_with_only_spaces(self):
        data = "    "
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_string_with_newline_characters(self):
        data = "\nNewLine\n"
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )

    def test_string_with_special_characters(self):
        data = "!@#$%^&*()_+-=[]{};':,.<>/?"
        self.assertEqual(
            data, decrypt_data(ENCRYPTION_KEY, encrypt_data(ENCRYPTION_KEY, data))
        )


if __name__ == "__main__":
    unittest.main()
