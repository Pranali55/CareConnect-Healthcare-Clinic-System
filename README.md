# CareConnect — Healthcare Clinic Management System

CareConnect is a Python portfolio project that demonstrates common outpatient clinic workflows using **FastAPI, SQLAlchemy, SQLite, Pydantic and HTML/CSS/JavaScript**.

It provides patient registration, doctor directory management, appointment scheduling, visit documentation and a clinic dashboard.

> **Demo and safety notice:** This repository is an educational portfolio project. Use only fictional sample data. It is not a diagnostic tool, emergency service, or production electronic health record (EHR). Do not enter real patient information.

## Features

- Clinic dashboard with patient, doctor, appointment and visit counts.
- Patient registration and patient directory.
- Doctor profiles with specialty and active status.
- Appointment scheduling and status updates.
- Prevents booking the same doctor's time slot twice.
- Visit records with symptoms/reason, clinical notes, prescription notes and follow-up date.
- SQLite database created automatically on first launch.
- Seeded fictional doctors, patients and appointments.
- FastAPI Swagger documentation.
- Automated API tests.

## Technology stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| API | FastAPI |
| ORM | SQLAlchemy 2 |
| Validation | Pydantic 2 |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Testing | unittest + FastAPI TestClient |

## Folder structure

```text
CareConnect-Healthcare-Clinic-System/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   └── static/
│       ├── index.html
│       ├── styles.css
│       └── app.js
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Windows setup

### Prerequisites

Install:
1. Python 3.10 or newer.
2. Visual Studio Code (recommended).
3. Git for GitHub upload.

Verify Python and Git from PowerShell:
```powershell
py --version
git --version
```

### 1. Extract and open the project

Extract `CareConnect-Healthcare-Clinic-System.zip`, open the extracted folder in VS Code, then open a PowerShell terminal in the project root.

### 2. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the FastAPI application

From the project root:
```powershell
uvicorn app.main:app --reload
```

Open:
- Clinic dashboard: http://127.0.0.1:8000
- Swagger API documentation: http://127.0.0.1:8000/docs
- ReDoc API documentation: http://127.0.0.1:8000/redoc
- Health endpoint: http://127.0.0.1:8000/api/health

The SQLite database file `careconnect.db` is created in the project root. It is ignored by Git. On the first run, the application inserts fictional demo doctors, patients and appointments.

## How to use the application

1. Open the dashboard.
2. Review the demo patients and doctors.
3. Register a new patient from the Patient Directory.
4. Add a doctor from the Care Team section.
5. Schedule an appointment using the dropdowns.
6. Change appointment status to Checked-in, Completed or Cancelled.
7. Add a visit record with notes and an optional follow-up date.
8. Review the dashboard counts.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | API health check |
| GET | `/api/dashboard` | Clinic dashboard metrics |
| GET / POST | `/api/patients` | List / register patients |
| GET / POST | `/api/doctors` | List / add doctors |
| GET / POST | `/api/appointments` | List / schedule appointments |
| PATCH | `/api/appointments/{id}/status` | Update appointment status |
| GET / POST | `/api/visits` | List / create visit records |

### Example: register a patient

```json
{
  "full_name": "Sample Patient",
  "date_of_birth": "1990-06-15",
  "gender": "Not specified",
  "phone": "9000000000",
  "email": "sample@example.test"
}
```

### Example: schedule an appointment

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "appointment_date": "2030-04-20",
  "appointment_time": "10:30:00",
  "reason": "Routine consultation"
}
```

### Example: create a visit record

```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "visit_date": "2030-04-20",
  "symptoms": "Demo reason for visit",
  "clinical_notes": "Fictional educational note",
  "prescription_notes": "No real prescription; sample text only",
  "follow_up_date": "2030-05-04"
}
```

## Testing

Install dependencies first, then from the project root run:
```powershell
python -m unittest discover -s tests -v
```

The test suite covers:
- API health response.
- Seeded demo records.
- Patient creation.
- Duplicate doctor appointment-slot conflict.
- Invalid appointment status validation.

For manual integration testing, run the application and use Swagger at `http://127.0.0.1:8000/docs`.

## GitHub upload guide

### 1. Create a repository

On GitHub, create a new **Public** repository named:

`CareConnect-Healthcare-Clinic-System`

Suggested description:

`Python FastAPI healthcare clinic management demo with patient registration, doctor directory, appointment scheduling, visit records, SQLite persistence and a responsive dashboard.`

Do not initialize the remote repository with another README or `.gitignore` because this project already includes both.

### 2. Push from Windows PowerShell

Run these commands from the project root:
```powershell
git init
git add .
git commit -m "Initial commit - CareConnect Healthcare Clinic System"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/CareConnect-Healthcare-Clinic-System.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

If Git says that `origin` already exists:
```powershell
git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/CareConnect-Healthcare-Clinic-System.git
git push -u origin main
```

Suggested repository topics:
`python`, `fastapi`, `healthcare`, `clinic-management`, `sqlite`, `sqlalchemy`, `rest-api`, `health-tech`.

## Resume / portfolio description

**CareConnect — Healthcare Clinic Management System**
- Developed a Python FastAPI application for outpatient clinic workflows, including patient registration, doctor directory, appointment scheduling and visit documentation.
- Designed relational data models and persistence using SQLAlchemy and SQLite.
- Implemented appointment slot conflict validation, Pydantic request validation and REST APIs.
- Built a responsive clinic dashboard using HTML, CSS and JavaScript, with automated API tests.

## Security, privacy and scope limitations

- The project is a local demo and has no user authentication, authorization, encryption, audit trail, backup/restore or production deployment configuration.
- The demo database contains fictional sample records only. Do not upload the SQLite database or real patient data to GitHub.
- Before any real-world use, conduct a privacy and security review and implement appropriate access control, encryption, consent, retention/deletion, audit logging, secure backups and compliance controls for the applicable jurisdiction.
- Clinical notes and prescription notes are plain text fields for workflow demonstration only. The application does not recommend medicines, diagnose conditions or validate clinical decisions.
