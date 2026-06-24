import pytest
import app as login_app


@pytest.fixture
def client():

    login_app.so_lan_sai = 0
    login_app.tai_khoan_bi_khoa = False
    login_app.thoi_gian_mo_khoa = 0

    login_app.app.config["TESTING"] = True

    with login_app.app.test_client() as client:
        yield client


def test_home(client):

    response = client.get("/")

    assert response.status_code == 200


def test_empty_email(client):

    response = client.post(
        "/api/login",
        json={
            "email": "",
            "password": "123"
        }
    )

    assert response.status_code == 400


def test_empty_password(client):

    response = client.post(
        "/api/login",
        json={
            "email": "K225480106099@tnut.edu.vn",
            "password": ""
        }
    )

    assert response.status_code == 400


def test_invalid_email(client):

    response = client.post(
        "/api/login",
        json={
            "email": "abcgmail.com",
            "password": "123"
        }
    )

    assert response.status_code == 400


def test_long_email(client):

    email = "a" * 101 + "@gmail.com"

    response = client.post(
        "/api/login",
        json={
            "email": email,
            "password": "123"
        }
    )

    assert response.status_code == 400


def test_login_success(client):

    response = client.post(
        "/api/login",
        json={
            "email": "K225480106099@tnut.edu.vn",
            "password": "123"
        }
    )

    assert response.status_code == 200


def test_wrong_password(client):

    response = client.post(
        "/api/login",
        json={
            "email": "K225480106099@tnut.edu.vn",
            "password": "abc123"
        }
    )

    assert response.status_code == 401


def test_lock_after_5_fail(client):

    for _ in range(5):

        response = client.post(
            "/api/login",
            json={
                "email": "K225480106099@tnut.edu.vn",
                "password": "SaiMatKhau"
            }
        )

    assert response.status_code == 403


def test_login_when_locked(client):

    for _ in range(5):

        client.post(
            "/api/login",
            json={
                "email": "K225480106099@tnut.edu.vn",
                "password": "SaiMatKhau"
            }
        )

    response = client.post(
        "/api/login",
        json={
            "email": "K225480106099@tnut.edu.vn",
            "password": "123"
        }
    )

    assert response.status_code == 403