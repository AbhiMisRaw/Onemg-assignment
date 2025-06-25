## User Management APIs

### Tech Stack


- **Backend**: FastAPI
- **ORM**: SQLAlcehmy
- **Database**: Postgres
- **Tools**: Swagger & Postman


### How to Run Project


#### Local Installation

1. create a directory and move to newwly created directory

```shell
mkdir user-management
cd user-management
```

2. Make an virtual environment and enable the virtual environment

```shell
# for windows
# creating virtual environment
python -m venv venv

# for linux or unix machine
# creating virtual environment
python3 -m venv venv
```

3. Clone the project

```bash
  git clone git@github.com:AbhiMisRaw/Onemg-assignment.git
```

4. Activate virtual environment.

```shell
# activating virtual environment for Windows
venv\Script\activate

# activating virtual environment for Unix-like Systems
source venv/bin/activate
```

5. Go to the cloned project directory

```bash
  cd user-management
```

6. Install dependencies

```bash
  pip install -r requirements.txt
```

7. Create `.env` file with following Values

```env
SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL=<DATABASE_URL>
```

8. Start the server

```bash
    uvicorn src.main:app
```

### API Endpoints


- If you are using _POSTMAN_ add **Authorization** header in **Headers** section for each request except `register` and `login` endpoints

```json
  KEY : "Authorization",
  Value : "Token <TOKEN STRING>"
```
- If you are using `curl`
```
curl -X GET http://127.0.0.1:8000/profile/1 -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

### For Registration
- Endpoints

 >   POST /register

- Body
```json
{
    "name":"USER_NAME",
    "email": "user@example.com",
    "password": "PASSWORD"
}
```
### For Signin
- Endpoints
 
> POST /api/auth/signin/

- Body
```json
{
    "email": "user@example.com",
    "password": "PASSWORD"
}
```

#### 1. Update the user’s profile based on the provided user ID.


> PUT /profile/{id}

**_REQUEST BODY_** 

> Include any field you want to Change.

```json
{
    "name": "Doe Doe", // OPTIONAL
    "email": "doe@example.com", // OPTIONAL
    "age": null, // OPTIONAL
    "city": null // OPTIONAL
}

```

**_RESPONSE_** 

```json
{
    "id": 2,
    "name": "Doe Doe",
    "email": "doe@example.com",
    "age": null,
    "city": null
}
```

{
    "id": 2,
    "name": "Doe Doe",
    "email": "doe@example.com",
    "age": null,
    "city": null
}


### Input Validation

- Used Pydanti's default Validation methods as well as some other validations.
- Email must be unique for each user.
- Password length must be 6 Character long.
- Age must be greater than 0 ( While updating.)


#### Running APIs

- **Register Request**

![Registeration](./pic/register_request.png "Registeration")

- **Login Request**

![Login](./pic/login_request.png "Login")


- **Get user by Id**

![Get Profile]( ./pic/get_request.png "Get Profile")

- **Update Profile**

![Update Profile](./pic/update_request.png "Update Request")