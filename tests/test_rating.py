import pytest

from tests.test_user import test_signup


# Testing Rating endpoints
@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_all_ratings(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

# Then, get the ratings
    response = client.get("/ratings/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_movie_rating(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Create movie
    movie_data = {"title": "Test Movie7", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08" 
                 }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie7"
    
    # Get movie_title
    movie_title = data['data']['title']

    response = client.get(f"/ratings/{movie_title}")
    assert response.status_code == 200
    data = response.json()
    assert data['data']['movie_title'] == "Test Movie7"
    assert "data" in data
    # assert isinstance(data, list)


@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_add_movie_ratings(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Create movie
    movie_data = {"title": "Test Movie8", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08" 
                 }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie8"
    
    # Get movie_title
    movie_title = data['data']['title']

    # Rate the movie
    rating_data = {"movie_rating": 8.0}
    response = client.post(
        f"/ratings?username={username}&movie_title={movie_title}",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Rating added successfully"
    assert data['data']['movie_rating'] == 8.0