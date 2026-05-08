def test_get_doctors(test_client):
    response = test_client.get("/doctors/")

    assert response.status_code == 200

    body = response.json()

    assert "data" in body
    assert isinstance(body["data"], list)


def test_doctor_search(test_client):
    response = test_client.get("/doctors/search?name=cardio")

    assert response.status_code == 200

    body = response.json()
    assert "data" in body


def test_doctor_filter(test_client):
    response = test_client.get("/doctors/search?specialization=Cardiology")

    assert response.status_code == 200
    assert "data" in response.json()


def test_doctor_pagination(test_client):
    response = test_client.get("/doctors/?skip=0&limit=2")

    assert response.status_code == 200

    body = response.json()
    assert len(body["data"]) <= 2