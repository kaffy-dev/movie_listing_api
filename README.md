# MOVIE LISTING API
This repository contains a movie listing API built using FastAPI. FastAPI is a python framework for building APIs. It comes with an interactive API documentation provided by Swagger UI for testing, documenting and visualizing APIs. You can read more on [FastAPI](https://fastapi.tiangolo.com/)

To install fastapi, ensure python is installed and then run the following command in your terminal.

```
pip install fastapi[all]
```
## Dependencies
All dependencies needed for this project is provided in the __requirements.txt file__. After cloning the repository, run the command below in your terminal to install all dependencies.

```
pip freeze > requirements.txt
```
## Cloning the Repository
To clone this repository, follow the steps below
- Go to the main page of the repository
- Click on `<>Code`
- Copy the URL for the repository
  - To clone the repository using HTTPS, under "HTTPS", 
  copy the URL
  - To clone the repository using an SSH key, including a 
   certificate issued by your organization's SSH 
   certificate authority, click SSH, then copy the URL
  - To clone a repository using GitHub CLI, click GitHub 
    CLI, then copy the URL
- Open your terminal
- Change the current working directory to the location 
  where you want the cloned directory.
- Type `git clone` and paste the URL you copied earlier
```
git clone https://github.com/kaffy-dev/movie_listing_api.git
```
## Features
This movie listing API allows users to list movies, view listed movies, add comments and rate the movies. It has the following features
- User Authentication
  - User registration
  - User login
  - JWT token generation: It is secured using JWT, ensuring 
    only users who created the movie can edit and delete 
    them.
- Movie Listing: Users can
  - list movies
  - view all movies
  - view a particular movie
  - edit a movie
  - delete a movie
- Comments: Users can
  - add comments
  - view comments for a movie
  - add nested comments
- Movie Rating: Users can
  - add rating for a movie
  - view movie rating

The API was developed using a SQL database, __PostgreSQL__ and __alembic__ was used for migraton. It includes logs managed on __papertrail__.

## Test
To execute the all tests on the endpoints, run the following command 
```
pytest tests
```
Use the command below to run test on individual file
```
pytest tests/<name_of_file>
Example: pytest tests/test_movie.py
```
To run the server, input the command `uvicorn main:app` in your terminal. Add `/docs` to the URL of the running server to access the API documentation provided by Swagger.
