import pytest

from tests.test_user import test_signup

# Testing comments endpoints
@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_comments(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Then, get all comments
    response = client.get("/comments/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_get_comment_for_a_movie(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Create movie
    movie_data = {"title": "Test Movie", "description": 
                  "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                 }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie"

    movie_id = data['data']['id']

    response = client.get(f"/comments/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_add_comment(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Create movie
    movie_data = {"title": "Test Movie4", "description": 
                  "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                 }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie4"

    movie_id = data['data']['id']

    # Add comment
    comment_data = {"content": "Nice movie"}
    response = client.post(f"/comments/?username={username}&movie_id={movie_id}", 
                           json=comment_data, 
                           headers={"Authorization": f"Bearer {token}"} 
                          )
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Comment added successfully"
    assert data['data']['content'] == "Nice movie"


@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_add_reply_to_existing_comment(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Create  movie
    movie_data = {"title": "Test Movie5", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                 }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie5"
    
    # Get movie_id
    movie_id = data['data']['id']

    # Add comment
    comment_data = {"content": "Nice movie"}
    response = client.post(f"/comments/?username={username}&movie_id={movie_id}", 
                           json=comment_data, 
                           headers={"Authorization": f"Bearer {token}"}
                          )
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Comment added successfully"
    assert data['data']['content'] == "Nice movie"
    
    # Get parent_comment_id
    parent_comment_id = data['data']['id']

    # Add reply
    nested_comment_data = {"reply": "I agree!"}
    response = client.post(
        f"/comments/nested_comment?reply_username={username}&parent_comment_id={parent_comment_id}",
        json=nested_comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Reply added successfully"
    assert data['data']['reply'] == "I agree!"


@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_add_reply_to_existing_reply(client, setup_database, username, password):
    # Login
    response = client.post("/users/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Create movie
    movie_data = {"title": "Test Movie6", 
                  "description": "An interesting movie", 
                  "duration": "120 minutes", 
                  "release_date": "2024-07-08"
                 }
    response = client.post("/movies/", json=movie_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "success"
    assert data['data']['title'] == "Test Movie6"

    # Get movie_id
    movie_id = data['data']['id']

    # Add comment
    comment_data = {"content": "Nice movie"}
    response = client.post(f"/comments/?username={username}&movie_id={movie_id}", 
                           json=comment_data, 
                           headers={"Authorization": f"Bearer {token}"}
                          )
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Comment added successfully"
    assert data['data']['content'] == "Nice movie"
    
    # Get parent_comment_id
    parent_comment_id = data['data']['id']

    # Add reply
    nested_comment_data = {"reply": "I agree!"}
    response = client.post(
        f"/comments/nested_comment?reply_username={username}&parent_comment_id={parent_comment_id}",
        json=nested_comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Reply added successfully"
    assert data['data']['reply'] == "I agree!"
    
    # Get parent_reply_id
    replies = data.get('data', {}).get('replies', [])
    if replies:
        parent_reply_id = replies[0].get('id')
        assert parent_reply_id is not None
        
        #  Add nested reply
        nested_reply_data = {"reply": "Yesss"}
        response = client.post(
           f"/comments/nested_reply?reply_username={username}&parent_reply_id={parent_reply_id}",
           json= nested_reply_data,
           headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data['message'] == "Reply added successfully"
        assert data['data']['reply'] == "Yesss"
