from datetime import date, time, timedelta
from sqlalchemy.orm import Session
from app.models import Appointment, Doctor, Patient

def seed_demo_data(db: Session):
    if db.query(Doctor).first():
        return
    doctors = [
        Doctor(full_name="Dr. Meera Joshi", specialty="General Medicine", phone="9000001001"),
        Doctor(full_name="Dr. Rahul Deshmukh", specialty="Pediatrics", phone="9000001002"),
        Doctor(full_name="Dr. Ananya Shah", specialty="Dermatology", phone="9000001003"),
    ]
    patients = [
        Patient(full_name="Demo Patient One", date_of_birth=date(1992,4,12), phone="9000002001", email="patient1@example.test"),
        Patient(full_name="Demo Patient Two", date_of_birth=date(1985,9,3), phone="9000002002", email="patient2@example.test"),
    ]
    db.add_all(doctors + patients)
    db.commit()
    tomorrow = date.today() + timedelta(days=1)
    db.add_all([
        Appointment(patient_id=patients[0].id, doctor_id=doctors[0].id, appointment_date=tomorrow, appointment_time=time(10,0), reason="Routine consultation"),
        Appointment(patient_id=patients[1].id, doctor_id=doctors[1].id, appointment_date=tomorrow, appointment_time=time(11,0), reason="Follow-up visit"),
    ])
    db.commit()
