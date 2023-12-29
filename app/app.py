from dotenv import load_dotenv
import base64

load_dotenv()

from flask import Flask, render_template, request
from flask_talisman import Talisman
from patient_data_encryption import encrypt_data, decrypt_data
import os

app = Flask(__name__, template_folder="../templates")
app.config["DEBUG"] = True


ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
# print("Encryption Key:", ENCRYPTION_KEY)

# Disable Flask-Talisman for local development
if os.environ.get("FLASK_ENV") != "development":
    Talisman(app)

print("Flask Debug Mode:", app.config["DEBUG"])


@app.route("/", methods=["GET", "POST"])
def home():
    encryption_status = ""
    encrypted_data_display = ""
    decrypted_data = ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "")

        if not user_input:
            encryption_status = "Input is empty."
        else:
            # Encrypt the user input
            encrypted_data = encrypt_data(user_input)

            # Convert bytes to string for display purposes
            encrypted_data_display = base64.b64encode(encrypted_data).decode()

            # Decrypt the encrypted data
            decrypted_data = decrypt_data(encrypted_data)

            if decrypted_data:
                encryption_status = "Encryption and decryption successful."
            else:
                encryption_status = "Decryption failed. Invalid data?"

    return render_template(
        "dashboard.html",
        encryption_status=encryption_status,
        encrypted_data=encrypted_data_display,
        decrypted_data=decrypted_data,
    )


if __name__ == "__main__":
    # print("Before running app")
    # print("FLASK_ENV:", os.environ.get("FLASK_ENV"))
    # print("app.debug:", app.debug)
    # print("app.config['DEBUG']:", app.config["DEBUG"])
    app.run(debug=True)


# /// basic hello world app for testing purposes ///
# from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def hello_world():
#     return "Hello, World!"


# if __name__ == "__main__":
#     print("Internal Debug Flag Before Running:", app.debug)
#     app.run(debug=True, port=5001)

#     print("Internal Debug Flag After Running:", app.debug)
