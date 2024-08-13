import pytest
from tests.test_user import test_signup


# Testing movie endpoints
@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_movies(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Then, get all movies
    response = client.get("/movies")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_create_movie(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Then, create a movie
    movie_data = {"title": "Test Movie", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                }
    response = client.post("/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie"

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_movie_by_id(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Create a movie
    movie_data = {"title": "Movie_test", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                }
    response = client.post("/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Movie_test"

    movie_id = data['data']['id']

    # Then, get movie by id
    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "success"
    assert "data" in data

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_movie_by_invalid_id(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Attempt to get a movie by an invalid ID
    movie_id = "00000000-0000-0000-0000-000000000000"  
    response = client.get(f"/movies/{movie_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Movie not found"


@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_movie_by_title(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Create a movie
    movie_data = {"title": "Movie_test2", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                }
    response = client.post("/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Movie_test2"

    movie_title = data['data']['title']

    # Then, get movie by title
    response = client.get(f"/movies/title/{movie_title}")
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "success"
    assert "data" in data

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_update_movie(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Create movie
    movie_data = {"title": "Test Movie2", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                  }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie2"
    
    # Get movie_id
    movie_id = data['data']['id']
    
    # Update movie
    updated_movie_data = {"title": "Updated Test Movie", 
                          "description": "A very interesting movie", 
                          "duration": "140 minutes", 
                          "release_date": "2024-07-24"
                         }
    response = client.put(f"/movies/{movie_id}", 
                          json=updated_movie_data, 
                          headers={"Authorization": f"Bearer {token}"}
                        )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["message"] == "Movie updated successfully"
    assert updated_data['data']['title'] == "Updated Test Movie"
    assert updated_data['data']['description'] == "A very interesting movie"
    assert updated_data['data']['duration'] == "140 minutes"
    assert updated_data['data']['release_date'] == "2024-07-24"


@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_delete_movie(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Create movie
    movie_data = {"title": "Test Movie3", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                 }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie3"

    # Get movie_id
    movie_id = data['data']['id']

    # Delete movie
    response = client.delete(f"/movies/{movie_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    
    # Verify the movie is deleted by trying to get it
    response = client.get(f"/movies/{movie_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "Movie not found"