from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -------------------------
# 1. TEST ROOT API
# -------------------------
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Advanced API Running"}


# -------------------------
# 2. TEST DOCTORS API
# -------------------------
def test_get_doctors():
    response = client.get("/doctors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -------------------------
# 3. TEST PATIENTS API (may fail if auth required)
# -------------------------
def test_get_patients():
    response = client.get("/patients/")
    # accept 200 or 401 depending on token
    assert response.status_code in [200, 401]


# -------------------------
# 4. TEST APPOINTMENT LIST
# -------------------------
def test_get_appointments():
    response = client.get("/appointments/")
    assert response.status_code in [200, 401]


# -------------------------
# 5. TEST PAGINATION
# -------------------------
def test_doctor_pagination():
    response = client.get("/doctors/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) <= 2


# -------------------------
# 6. TEST SEARCH FILTER
# -------------------------
def test_doctor_filter():
    response = client.get("/doctors/?specialization=Cardiology")
    assert response.status_code == 200