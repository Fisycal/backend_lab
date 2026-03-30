# Backend Concepts Lab

A hands-on backend engineering project demonstrating core concepts such as REST APIs, HTTP methods, authentication, authorization, and data validation using FastAPI.

---

## 🚀 Project Overview

This project is designed to build a strong foundation in backend development by implementing real-world concepts step by step:

* API design and REST principles
* HTTP methods and status codes
* JWT (stateless authentication)
* Session-based authentication (stateful)
* Role-based authorization (admin vs user)
* Request/response validation using Pydantic

---

## 📦 Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **Passlib (bcrypt)** – password hashing
* **python-jose** – JWT handling
* **Uvicorn** – ASGI server

---

## 🧱 Project Structure

```
app/
├── main.py
├── trial_data.py              # In-memory user data (temporary)
├── schemas/                   # Pydantic models
│   ├── user.py
│   └── auth.py
├── routes/                    # API routes
│   ├── users.py
│   └── auth.py
├── utils/                     # Helper utilities
│   ├── jwt_handler.py
│   ├── password.py
│   └── session_store.py
```

---

## 🔑 Features Implemented

### ✅ 1. RESTful API (Users)

| Method | Endpoint      | Description           |
| ------ | ------------- | --------------------- |
| GET    | `/users/`     | Get all users         |
| GET    | `/users/{id}` | Get user by ID        |
| POST   | `/users/`     | Create new user       |
| PUT    | `/users/{id}` | Replace user          |
| PATCH  | `/users/{id}` | Partially update user |
| DELETE | `/users/{id}` | Delete user           |

---

### ✅ 2. HTTP Methods Covered

* GET
* POST
* PUT
* PATCH
* DELETE
* HEAD
* OPTIONS

---

### ✅ 3. HTTP Status Codes Used

| Code | Meaning              |
| ---- | -------------------- |
| 200  | OK                   |
| 201  | Created              |
| 204  | No Content           |
| 400  | Bad Request          |
| 401  | Unauthorized         |
| 403  | Forbidden            |
| 404  | Not Found            |
| 422  | Unprocessable Entity |

---

### 🔐 4. Authentication

#### JWT Authentication (Stateless)

* `POST /auth/login-jwt` → returns access token
* `GET /auth/me-jwt` → get current user
* `GET /auth/protected-jwt` → protected route

JWT is sent via:

```
Authorization: Bearer <token>
```

---

#### Session Authentication (Stateful)

* `POST /auth/login-session` → sets session cookie
* `GET /auth/me-session` → retrieves current session
* `POST /auth/logout-session` → clears session

Sessions are stored server-side and managed via cookies.

---

### 🛡️ 5. Authorization (Role-Based Access)

* `GET /auth/admin-jwt` → accessible only by admin users

#### Behavior:

* Valid admin → `200 OK`
* Valid user (non-admin) → `403 Forbidden`
* No token → `401 Unauthorized`

---

## ⚖️ Key Concepts Demonstrated

### Authentication vs Authorization

* **Authentication** → Who are you? (Login)
* **Authorization** → What can you do? (Admin access)

---

### Stateless vs Stateful APIs

| Type    | Description                  |
| ------- | ---------------------------- |
| JWT     | Stateless (no server memory) |
| Session | Stateful (stored on server)  |

---

### Session vs JWT

| Feature     | JWT    | Session         |
| ----------- | ------ | --------------- |
| Storage     | Client | Server          |
| Auto-send   | ❌ No   | ✅ Yes (cookies) |
| Scalability | High   | Lower           |
| Revocation  | Harder | Easier          |

---

## 🧪 Validation with Pydantic

All request bodies are validated using Pydantic models.

### Example

```json
{
  "email": "invalid-email",
  "password": "admin123"
}
```

Response:

```
422 Unprocessable Entity
```

---

## 🛠️ How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd backend-concepts-lab
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

### 5. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

## 📸 Screenshots

### Swagger UI

<img src="screenshots/swagger-home.png" width="800"/>
<img src="screenshots/swagger-home-auth.png" width="800"/>
<img src="screenshots/swagger-home-schemas.png" width="800"/>


### JWT Login
<img src="screenshots/jwt-login.png" width="800"/>


### Authenticated User (JWT)
<img src="screenshots/me-jwt.png" width="800"/>


### Admin Authorization
<img src="screenshots/admin-route.png" width="800"/>

---

## 🧠 Key Learnings

* Building RESTful APIs from scratch
* Handling HTTP requests and responses
* Implementing authentication (JWT + session)
* Managing authorization (role-based access)
* Debugging real-world dependency issues (`bcrypt` + `passlib`)
* Structuring backend projects properly
* Validating input using Pydantic

---

## ⚠️ Known Limitations

* Uses in-memory data (`trial_data.py`) instead of a real database
* No token refresh mechanism yet
* No persistent user storage

---

## 🚀 Next Steps (Milestone 4)

* Add a real database (SQLite → PostgreSQL)
* Use SQLAlchemy ORM
* Store users persistently
* Improve authentication system

---

## 👨‍💻 Michael Ogunsanya

Built as part of a hands-on backend engineering learning journey.

---
