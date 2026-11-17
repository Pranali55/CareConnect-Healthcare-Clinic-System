from datetime import date
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Appointment, Doctor, Patient, Visit
from app.schemas import (
    AppointmentCreate, AppointmentOut, AppointmentStatusUpdate,
    DoctorCreate, DoctorOut, PatientCreate, PatientOut, VisitCreate, VisitOut
)
from app.seed import seed_demo_data

app = FastAPI(
    title="CareConnect Healthcare Clinic API",
    description="Clinic workflow demo for patient registration, doctors, appointments and visit notes.",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)
with next(get_db()) as startup_db:
    seed_demo_data(startup_db)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "CareConnect API"}

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    today = date.today()
    return {
        "total_patients": db.query(Patient).count(),
        "active_doctors": db.query(Doctor).filter(Doctor.is_active.is_(True)).count(),
        "appointments_today": db.query(Appointment).filter(Appointment.appointment_date == today).count(),
        "upcoming_appointments": db.query(Appointment).filter(Appointment.appointment_date >= today, Appointment.status == "Scheduled").count(),
        "total_visits": db.query(Visit).count()
    }

@app.get("/api/patients", response_model=list[PatientOut])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).order_by(Patient.full_name).all()

@app.post("/api/patients", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@app.get("/api/doctors", response_model=list[DoctorOut])
def list_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).filter(Doctor.is_active.is_(True)).order_by(Doctor.full_name).all()

@app.post("/api/doctors", response_model=DoctorOut, status_code=status.HTTP_201_CREATED)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(**payload.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

@app.get("/api/appointments", response_model=list[AppointmentOut])
def list_appointments(db: Session = Depends(get_db)):
    rows = db.query(Appointment).all()
    return [
        AppointmentOut(
            id=a.id, patient_id=a.patient_id, doctor_id=a.doctor_id,
            appointment_date=a.appointment_date, appointment_time=a.appointment_time,
            reason=a.reason, status=a.status, patient_name=a.patient.full_name,
            doctor_name=a.doctor.full_name
        ) for a in sorted(rows, key=lambda x: (x.appointment_date, x.appointment_time))
    ]

@app.post("/api/appointments", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, payload.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found.")
    if not db.get(Doctor, payload.doctor_id):
        raise HTTPException(status_code=404, detail="Doctor not found.")
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="This doctor already has an appointment at that date and time.")
    db.refresh(appointment)
    return AppointmentOut(
        id=appointment.id, patient_id=appointment.patient_id, doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date, appointment_time=appointment.appointment_time,
        reason=appointment.reason, status=appointment.status,
        patient_name=appointment.patient.full_name, doctor_name=appointment.doctor.full_name
    )

@app.patch("/api/appointments/{appointment_id}/status")
def update_appointment_status(appointment_id: int, payload: AppointmentStatusUpdate, db: Session = Depends(get_db)):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    appointment.status = payload.status
    db.commit()
    return {"id": appointment.id, "status": appointment.status}

@app.get("/api/visits", response_model=list[VisitOut])
def list_visits(db: Session = Depends(get_db)):
    rows = db.query(Visit).order_by(Visit.visit_date.desc()).all()
    return [
        VisitOut(
            id=v.id, patient_id=v.patient_id, doctor_id=v.doctor_id, visit_date=v.visit_date,
            symptoms=v.symptoms, clinical_notes=v.clinical_notes,
            prescription_notes=v.prescription_notes, follow_up_date=v.follow_up_date,
            patient_name=v.patient.full_name, doctor_name=v.doctor.full_name
        ) for v in rows
    ]

@app.post("/api/visits", response_model=VisitOut, status_code=status.HTTP_201_CREATED)
def create_visit(payload: VisitCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, payload.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found.")
    if not db.get(Doctor, payload.doctor_id):
        raise HTTPException(status_code=404, detail="Doctor not found.")
    visit = Visit(**payload.model_dump())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return VisitOut(
        id=visit.id, patient_id=visit.patient_id, doctor_id=visit.doctor_id,
        visit_date=visit.visit_date, symptoms=visit.symptoms,
        clinical_notes=visit.clinical_notes, prescription_notes=visit.prescription_notes,
        follow_up_date=visit.follow_up_date, patient_name=visit.patient.full_name,
        doctor_name=visit.doctor.full_name
    )
