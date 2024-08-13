import pytest

# Registration Tests
@pytest.mark.parametrize("username, password, full_name", [("testuser", "testpassword", "Test User")])
def test_signup(client, setup_database, username, password, full_name):
    # Sign up the user
    response = client.post(
        "/users/signup", 
        json={"username": username, 
        "password": password,
        "full_name": full_name}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == username


@pytest.mark.parametrize("username, password, full_name", [("testuser2", "testpassword", "Test User")])
def test_login(client, setup_database, username, password, full_name):
    # First, sign up the user
    response = client.post("/users/signup", 
                           json={"username": username, 
                           "password": password, 
                           "full_name": full_name}
                          )
    assert response.status_code == 200

    # Then, login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"