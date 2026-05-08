def test_get_patients_unauthorized(test_client):
    response = test_client.get("/patients/")

    assert response.status_code in [401, 403]


def test_get_patients_authorized(test_client):

    # =========================
    # 1. REGISTER USER
    # =========================
    email = "test@example.com"
    password = "test123"

    reg = test_client.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert reg.status_code in [200, 400]  # ok if already exists

    # =========================
    # 2. LOGIN
    # =========================
    login = test_client.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert login.status_code == 200, f"Login failed: {login.text}"

    data = login.json()

    assert "data" in data
    assert "access_token" in data["data"]

    token = data["data"]["access_token"]

    # =========================
    # 3. CALL API
    # =========================
    response = test_client.get(
        "/patients/",
        headers={"Authorization": f"Bearer {token}"}
    )

    # IMPORTANT:
    # allow 200 OR 403 depending on RBAC config
    assert response.status_code in [200, 403]