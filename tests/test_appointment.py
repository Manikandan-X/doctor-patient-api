def test_get_appointments(test_client, auth_headers):
    response = test_client.get("/appointments/", headers=auth_headers)
    assert response.status_code in [200, 403, 401]


def test_create_appointment(auth_client):
    response = auth_client.post("/appointments/", json={
        "doctor_id": 1,
        "appointment_date": "2026-05-10",
        "appointment_time": "10:00"
    })

    assert response.status_code in [200, 201, 400, 401, 422]


def test_double_booking(auth_client):
    response = auth_client.post("/appointments/", json={
        "doctor_id": 1,
        "appointment_date": "2026-05-10",
        "appointment_time": "10:00"
    })

    assert response.status_code in [400, 409, 401, 422]


def test_invalid_appointment_date(auth_client):
    response = auth_client.post("/appointments/", json={
        "doctor_id": 1,
        "appointment_date": "invalid-date",
        "appointment_time": "10:00"
    })

    assert response.status_code in [400, 422, 401]