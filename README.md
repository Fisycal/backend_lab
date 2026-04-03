# 🚀 Backend Concepts Lab

A production-style backend engineering project built with **FastAPI** to demonstrate core backend concepts through hands-on implementation, including REST APIs, authentication, authorization, validation, database persistence, environment-based configuration, and schema migrations.

---

## 📚 Project Progression

This project was built incrementally:

* Milestone 1: API fundamentals (REST, HTTP methods)
* Milestone 2: Authentication & Authorization
* Milestone 3: Validation with Pydantic
* Milestone 4: Database integration (SQLAlchemy)
* Milestone 5: Environment config + Alembic migrations

---

## 📌 Overview

This project was created as a practical backend engineering lab to learn and implement real-world backend concepts step by step.

It currently demonstrates:

* RESTful API design
* HTTP methods and status codes
* JWT authentication (stateless)
* Session-based authentication (stateful)
* Role-based authorization
* Request validation using Pydantic
* Persistent data storage using SQLAlchemy + SQLite
* Environment-based configuration using `.env`
* Database schema versioning with Alembic

---

## 🧱 Architecture

```text
Client (Swagger / Postman)
        ↓
FastAPI Routes
        ↓
Validation (Pydantic)
        ↓
Business Logic
        ↓
SQLAlchemy ORM
        ↓
SQLite Database
        ↑
Alembic Migrations
```

---

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **SQLite**
* **Alembic**
* **Pydantic**
* **pydantic-settings**
* **Passlib (bcrypt)** – password hashing
* **python-jose** – JWT creation and verification
* **Uvicorn**

---

## 📂 Project Structure

```text
app/
├── main.py
├── config.py                  # Application settings from .env
├── db/
│   ├── database.py            # Engine, session, Base, DB dependency
│   └── models.py              # SQLAlchemy models
├── schemas/
│   ├── user.py                # User request/response schemas
│   └── auth.py                # Auth request/response schemas
├── routes/
│   ├── users.py               # User CRUD routes
│   └── auth.py                # Auth + protected routes
├── utils/
│   ├── jwt_handler.py         # JWT encode/decode logic
│   ├── password.py            # Password hashing / verification
│   └── session_store.py       # In-memory session store (learning purpose)

alembic/
├── env.py                     # Alembic environment config
├── script.py.mako
└── versions/                  # Migration files

.env.example
alembic.ini
requirements.txt
README.md
```

---

## 🔑 Features

### ✅ RESTful User API

| Method  | Endpoint      | Description                     |
| ------- | ------------- | ------------------------------- |
| GET     | `/users/`     | Get all users                   |
| GET     | `/users/{id}` | Get user by ID                  |
| POST    | `/users/`     | Create user                     |
| PUT     | `/users/{id}` | Replace user                    |
| PATCH   | `/users/{id}` | Partially update user           |
| DELETE  | `/users/{id}` | Delete user                     |
| HEAD    | `/users/`     | Check collection headers        |
| HEAD    | `/users/{id}` | Check single user headers       |
| OPTIONS | `/users/`     | Allowed methods for collection  |
| OPTIONS | `/users/{id}` | Allowed methods for single user |

---

### 🔐 Authentication

#### JWT Authentication (Stateless)

* `POST /auth/login-jwt` → returns access token
* `GET /auth/me-jwt` → current authenticated user
* `GET /auth/protected-jwt` → protected route
* `GET /auth/admin-jwt` → admin-only route

JWT is sent via:

```text
Authorization: Bearer <token>
```

---

#### Session Authentication (Stateful)

* `POST /auth/login-session`
* `GET /auth/me-session`
* `POST /auth/logout-session`

Sessions are stored server-side and tracked via cookies.

---

### 🛡️ Authorization

Authorization is role-based.

The `admin-jwt` route checks the `role` stored in the JWT payload.

#### Expected behavior

| Scenario                | Result           |
| ----------------------- | ---------------- |
| Valid admin token       | 200 OK           |
| Valid non-admin token   | 403 Forbidden    |
| Missing token           | 401 Unauthorized |
| Invalid / expired token | 401 Unauthorized |

---

## 🗄️ Database

This project uses **SQLite** for development.

### Current user model fields

* `id`
* `name`
* `email`
* `password` (hashed)
* `role`

User records are persisted in the database and survive application restarts.

---

## 🔄 Database Migrations (Alembic)

This project uses **Alembic** to manage database schema changes.

### Why Alembic was added

Before Alembic, schema creation depended on `Base.metadata.create_all(...)`, which is okay for early prototyping but not ideal for real projects.

Alembic provides:

* version-controlled schema changes
* safer database evolution
* repeatable migration workflow
* better team/project collaboration

### Migration workflow

Generate migration:

```bash
alembic revision --autogenerate -m "create users table"
```

Apply migration:

```bash
alembic upgrade head
```

Check current revision:

```bash
alembic current
```

---

## ⚙️ Environment Configuration

Application settings are managed using `.env` and `pydantic-settings`.

### Example `.env.example`

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Why this matters

This prevents hardcoded secrets and makes the app easier to configure across environments.

Used for:

* database connection URL
* JWT secret key
* JWT algorithm
* token expiration time

---

## 🔐 Security

* Passwords are hashed using **bcrypt**
* JWT secrets are loaded from environment variables
* Passwords are never returned in API responses
* Admin access is controlled via user roles
* Session cookies are `httponly`

---

## ✅ Validation

This project uses **Pydantic** models for request and response validation.

Validation examples include:

* required fields
* valid email format
* password minimum length
* structured request bodies

Typical validation error:

```text
422 Unprocessable Entity
```

---

## 🌐 Important Backend Concepts Demonstrated

### Authentication vs Authorization

* **Authentication** → verifies identity
* **Authorization** → checks permissions

### Stateless vs Stateful

| Type    | Description                     |
| ------- | ------------------------------- |
| JWT     | Stateless; client carries token |
| Session | Stateful; server stores session |

### HTTP Status Codes Used

| Code | Meaning          |
| ---- | ---------------- |
| 200  | OK               |
| 201  | Created          |
| 204  | No Content       |
| 400  | Bad Request      |
| 401  | Unauthorized     |
| 403  | Forbidden        |
| 404  | Not Found        |
| 422  | Validation Error |

---

## 📸 Screenshots

### Swagger UI

<img src="screenshots/swagger-home.png" width="800"/>

### JWT Login

<img src="screenshots/jwt-login.png" width="800"/>

### Authenticated User

<img src="screenshots/me-jwt.png" width="800"/>

### Admin Authorization

<img src="screenshots/admin-route.png" width="800"/>

---

## 🧪 How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd backend-core-concepts
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Copy `.env.example` to `.env` and provide your values.

### 5. Apply migrations

```bash
alembic upgrade head
```

### 6. Run the app

```bash
uvicorn app.main:app --reload
```

### 7. Open API docs

```text
http://127.0.0.1:8000/docs
```

---

## ❤️ Health Check

A simple health endpoint is available:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## ⚠️ Known Limitations

* SQLite is used for development only
* Session storage is in-memory and not shared across instances
* No refresh token workflow yet
* No background jobs or async task queue yet
* No Docker/deployment setup yet

---

## 🚀 Future Improvements

* Docker support
* PostgreSQL integration
* Redis-backed sessions
* Refresh tokens
* Role management improvements
* Deployment to Render / Railway / AWS
* CI/CD pipeline
* Automated tests expansion

---

## 🧠 Key Learnings

This project helped reinforce:

* building RESTful APIs from scratch
* proper use of HTTP methods and status codes
* request and response validation
* password hashing and JWT-based auth
* session-based auth comparison
* environment-based configuration
* schema migrations with Alembic
* debugging real backend errors across auth, DB, and config

---

## 👨‍💻 Author

Backend engineering learning project built with a focus on practical implementation, production mindset, and long-term portfolio value.
