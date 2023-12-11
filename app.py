from flask import Flask, render_template, request
from flask_talisman import Talisman
from patient_data_encryption import encrypt_data, decrypt_data
from encryption_config import ENCRYPTION_KEY

app = Flask(__name__)


# Set the environment to 'development' for local development
app.config["ENV"] = "development"

# Disable Flask-Talisman for local development
if app.config["ENV"] != "development":
    Talisman(app)


@app.route("/", methods=["GET", "POST"])
def home():
    encryption_status = ""
    decrypted_data = ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "")

        # Check if the user input is empty
        if not user_input:
            encryption_status = "Input is empty."
        else:
            # Encrypt the user input
            encrypted_data = encrypt_data(ENCRYPTION_KEY, user_input)

            # Decrypt the encrypted data
            decrypted_data = decrypt_data(ENCRYPTION_KEY, encrypted_data)

            # Check if decryption was successful
            if decrypted_data:
                encryption_status = "Encryption and decryption successful."
            else:
                encryption_status = "Decryption failed. Invalid data?"

    return render_template(
        "dashboard.html",
        encryption_status=encryption_status,
        decrypted_data=decrypted_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
