import os
import tempfile
import unittest

db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
db_file.close()
os.environ["DATABASE_URL"] = f"sqlite:///{db_file.name}"

from fastapi.testclient import TestClient
from app.main import app

class CareConnectApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_seeded_demo_records(self):
        self.assertGreaterEqual(len(self.client.get("/api/doctors").json()), 1)
        self.assertGreaterEqual(len(self.client.get("/api/patients").json()), 1)

    def test_create_patient(self):
        response = self.client.post("/api/patients", json={
            "full_name": "Test Person", "gender": "Not specified",
            "phone": "9000000000", "email": "test.person@example.test"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["full_name"], "Test Person")

    def test_doctor_slot_conflict(self):
        patient = self.client.post("/api/patients", json={"full_name": "Conflict Patient"}).json()
        doctor = self.client.get("/api/doctors").json()[0]
        payload = {
            "patient_id": patient["id"], "doctor_id": doctor["id"],
            "appointment_date": "2035-05-05", "appointment_time": "09:15:00",
            "reason": "Test slot"
        }
        self.assertEqual(self.client.post("/api/appointments", json=payload).status_code, 201)
        self.assertEqual(self.client.post("/api/appointments", json=payload).status_code, 409)

    def test_invalid_status_rejected(self):
        response = self.client.patch("/api/appointments/999/status", json={"status": "Unknown"})
        self.assertIn(response.status_code, (404, 422))

if __name__ == "__main__":
    unittest.main()
