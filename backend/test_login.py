from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Student-specific test data created specifically for this assignment.
TEST_EMAIL = "vivek.pytest@nexstep.example"
TEST_PASSWORD = "Vivek@123"


def test_valid_student_login():
    """
    PT-01: Verify that a registered student can log in
    using valid credentials.
    """
    response = client.post(
        "api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data
    assert data["token"]
    assert "user" in data
    assert data["user"]["email"] == TEST_EMAIL
    assert "hasProfile" in data


def test_invalid_student_login():
    """
    PT-02: Negative test - verify that login fails
    when an incorrect password is supplied.
    """
    response = client.post(
        "api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Incorrect email or password"