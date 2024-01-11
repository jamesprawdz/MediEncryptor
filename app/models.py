from . import db
from sqlalchemy.dialects.postgresql import JSONB

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(1))
    address = db.Column(db.Text)
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    prescription_history = db.Column(db.Text)
    insurance_info = db.Column(JSONB)
