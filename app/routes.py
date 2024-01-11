from flask import jsonify, request
import logging
import json
from datetime import datetime
from . import app, db, ENCRYPTION_KEY
from .models import Patient
from .patient_data_encryption import encrypt_data, decrypt_data

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/add_patient", methods=["POST"])
def add_patient():
    # Log that a request was received
    logging.debug("Received request to /add_patient")

    # Log the form data for debugging purposes
    logging.debug("Form Data: %s", request.form)

    try:
        print("Arguments for encrypt_data - Address:", request.form.get("address"))
        print("Arguments for encrypt_data - ENCRYPTION_KEY:", ENCRYPTION_KEY)
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth_str = request.form.get("date_of_birth")
        date_of_birth = (
            datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
            if date_of_birth_str
            else None
        )
        gender = request.form.get("gender")
        address = encrypt_data(request.form.get("address"), ENCRYPTION_KEY)
        email = encrypt_data(request.form.get("email"), ENCRYPTION_KEY)
        phone_number = encrypt_data(request.form.get("phone_number"), ENCRYPTION_KEY)
        medical_history = encrypt_data(
            request.form.get("medical_history"), ENCRYPTION_KEY
        )
        prescription_history = encrypt_data(
            request.form.get("prescription_history"), ENCRYPTION_KEY
        )
        insurance_info_str = request.form.get(
            "insurance_info"
        )  # Assuming this is a string field
        insurance_info = json.loads(insurance_info_str) if insurance_info_str else {}

        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            email=email,
            phone_number=phone_number,
            medical_history=medical_history,
            prescription_history=prescription_history,
            insurance_info=insurance_info,
        )

        db.session.add(new_patient)
        db.session.commit()

        # Log success and return response
        logging.debug("New patient added successfully")
        return jsonify({"message": "New patient added"}), 201

    except Exception as e:
        # Log any exception that occurs
        logging.error("An error occurred: %s", e)
        return jsonify({"message": str(e)}), 500


@app.route("/edit_patient/<int:id>", methods=["PUT"])
def edit_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    data = request.json
    patient.first_name = data.get("first_name", patient.first_name)
    patient.last_name = data.get("last_name", patient.last_name)
    patient.date_of_birth = data.get("date_of_birth", patient.date_of_birth)
    patient.gender = data.get("gender", patient.gender)
    patient.address = encrypt_data(data.get("address", patient.address), ENCRYPTION_KEY)
    patient.email = encrypt_data(data.get("email", patient.email), ENCRYPTION_KEY)
    patient.phone_number = encrypt_data(
        data.get("phone_number", patient.phone_number), ENCRYPTION_KEY
    )
    patient.medical_history = encrypt_data(
        data.get("medical_history", patient.medical_history), ENCRYPTION_KEY
    )
    patient.prescription_history = encrypt_data(
        data.get("prescription_history", patient.prescription_history), ENCRYPTION_KEY
    )
    patient.insurance_info = data.get("insurance_info", patient.insurance_info)

    db.session.commit()
    return jsonify({"message": "Patient updated"}), 200


@app.route("/delete_patient/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted"}), 200


@app.route("/patient/<int:id>", methods=["GET"])
def get_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    patient_data = {
        "id": patient.id,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "date_of_birth": patient.date_of_birth.isoformat()
        if patient.date_of_birth
        else None,
        "gender": patient.gender,
        "address": decrypt_data(patient.address, ENCRYPTION_KEY),
        "email": decrypt_data(patient.email, ENCRYPTION_KEY),
        "phone_number": decrypt_data(patient.phone_number, ENCRYPTION_KEY),
        "medical_history": decrypt_data(patient.medical_history, ENCRYPTION_KEY),
        "prescription_history": decrypt_data(
            patient.prescription_history, ENCRYPTION_KEY
        ),
        "insurance_info": patient.insurance_info,
    }
    return jsonify(patient_data), 200


@app.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    patient_list = []
    for patient in patients:
        patient_data = {
            "id": patient.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "date_of_birth": patient.date_of_birth.isoformat()
            if patient.date_of_birth
            else None,
            "gender": patient.gender,
            "address": decrypt_data(patient.address, ENCRYPTION_KEY),
            "email": decrypt_data(patient.email, ENCRYPTION_KEY),
            "phone_number": decrypt_data(patient.phone_number, ENCRYPTION_KEY),
            "medical_history": decrypt_data(patient.medical_history, ENCRYPTION_KEY),
            "prescription_history": decrypt_data(
                patient.prescription_history, ENCRYPTION_KEY
            ),
            "insurance_info": patient.insurance_info,
        }
        patient_list.append(patient_data)
    return jsonify(patient_list), 200
