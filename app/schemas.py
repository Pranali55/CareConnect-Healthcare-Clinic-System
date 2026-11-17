from datetime import date, time
from pydantic import BaseModel, ConfigDict, Field, field_validator

class PatientCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    date_of_birth: date | None = None
    gender: str = Field(default="Not specified", max_length=30)
    phone: str = Field(default="", max_length=30)
    email: str = Field(default="", max_length=160)

class PatientOut(PatientCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class DoctorCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    specialty: str = Field(min_length=2, max_length=100)
    phone: str = Field(default="", max_length=30)

class DoctorOut(DoctorCreate):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str = Field(default="", max_length=250)

class AppointmentStatusUpdate(BaseModel):
    status: str
    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        allowed = {"Scheduled", "Checked-in", "Completed", "Cancelled"}
        if value not in allowed:
            raise ValueError(f"Status must be one of: {', '.join(sorted(allowed))}")
        return value

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str
    status: str
    patient_name: str
    doctor_name: str

class VisitCreate(BaseModel):
    patient_id: int
    doctor_id: int
    visit_date: date
    symptoms: str = Field(default="", max_length=3000)
    clinical_notes: str = Field(default="", max_length=5000)
    prescription_notes: str = Field(default="", max_length=3000)
    follow_up_date: date | None = None

class VisitOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    visit_date: date
    symptoms: str
    clinical_notes: str
    prescription_notes: str
    follow_up_date: date | None
    patient_name: str
    doctor_name: str
