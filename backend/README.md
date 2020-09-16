# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!
    

## API


GET '/drinks'
- Fetches a dictionary of drinks in which the keys are the ids, title and recipe
- *Request Arguments:* None
```
{
    "drinks": [
        {
            "id": 1,
            "recipe": {
                "color": "blue",
                "parts": 1
            },
            "title": "Water3"
        }
    ],
    "success": true
}
```

GET '/drinks-detail'
- Fetches a dictionary of drinks in which the keys are the ids, title, name and recipe
- *Request parameters:* get:drinks-detail permission
- *Example response:* 
 ``` 
{
    "drinks": [
        {
            "id": 1,
            "recipe": {
                "color": "blue",
                "name": "Water",
                "parts": 1
            },
            "title": "Water3"
        }
    ],
    "success": true
}
```

POST `/drinks`
- Add a new drink to the repository of available drinks
- *Request arguments:* post:drinks permission
- *Example response:* 
```
{
    "drinks": [
        {
            "id": 2,
            "recipe": {
                "color": "blue",
                "name": "Water",
                "parts": 1
            },
            "title": "Water6"
        }
    ],
    "success": true
}
```

PATCH `/drinks/<int:id>`
- Update a parameter of a specific drink 
- *Request arguments:* int:id and patch:drinks permission
- *Example response:* 
```
{
    "drink": [
        {
            "id": 1,
            "recipe": {
                "color": "blue",
                "name": "Water",
                "parts": 1
            },
            "title": "Water5"
        }
    ],
    "success": true
}
```
DELETE `/drinks/<int:id>`
- Delete a specific drink 
- *Request arguments:* int:id and delete:drinks permission
- *Example response:*
```
{
    "delete": [
        1
    ],
    "success": true
}
```

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
