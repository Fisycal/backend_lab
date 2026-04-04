# 🚀 Backend Concepts Lab

A production-style backend engineering project built with **FastAPI** to demonstrate core backend concepts through hands-on implementation — including REST APIs, authentication, validation, database persistence, environment configuration, migrations, and containerization.

---

## 📚 Project Progression

This project was built incrementally:

* Milestone 1: API fundamentals (REST, HTTP methods)
* Milestone 2: Authentication & Authorization
* Milestone 3: Validation with Pydantic
* Milestone 4: Database integration (SQLAlchemy)
* Milestone 5: Environment config + Alembic migrations
* Milestone 6: Docker + Docker Compose + Volume persistence

---

## 📌 Overview

This project demonstrates how to build a **real-world backend system** step-by-step.

Key capabilities:

* RESTful API design
* JWT (stateless) and session (stateful) authentication
* Role-based authorization
* Input validation using Pydantic
* Persistent storage using SQLAlchemy + SQLite
* Environment-based configuration using `.env`
* Database schema migrations using Alembic
* Containerization using Docker
* Multi-container orchestration using Docker Compose
* Volume-based database persistence

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
        ↑
Docker Container
        ↑
Docker Compose (with volume)
```

---

## 🛠️ Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Alembic
* Pydantic
* pydantic-settings
* Passlib (bcrypt)
* python-jose (JWT)
* Uvicorn
* Docker
* Docker Compose

---

## 📂 Project Structure

```text
app/
├── main.py
├── config.py
├── db/
│   ├── database.py
│   └── models.py
├── schemas/
│   ├── user.py
│   └── auth.py
├── routes/
│   ├── users.py
│   └── auth.py
├── utils/
│   ├── jwt_handler.py
│   ├── password.py
│   └── session_store.py

alembic/
├── env.py
├── versions/

.env.example
Dockerfile
docker-compose.yml
alembic.ini
requirements.txt
README.md
```

---

## 🔑 Features

### ✅ RESTful API

* Full CRUD for users
* Supports GET, POST, PUT, PATCH, DELETE
* Includes HEAD and OPTIONS methods

---

### 🔐 Authentication

#### JWT (Stateless)

* `POST /auth/login-jwt`
* `GET /auth/me-jwt`
* `GET /auth/admin-jwt`

Uses:

```text
Authorization: Bearer <token>
```

---

#### Session (Stateful)

* `POST /auth/login-session`
* `GET /auth/me-session`
* `POST /auth/logout-session`

---

### 🛡️ Authorization

Role-based access control:

* `admin` → full access
* `user` → limited access

---

## 🗄️ Database

* SQLite (development)
* SQLAlchemy ORM
* Data persists across container restarts via volume mount

---

## 🔄 Database Migrations (Alembic)

Generate migration:

```bash
alembic revision --autogenerate -m "create users table"
```

Apply migration:

```bash
alembic upgrade head
```

Run inside Docker:

```bash
docker compose exec app alembic upgrade head
```

---

## ⚙️ Environment Configuration

`.env` controls runtime settings:

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Never commit `.env` to GitHub.

---

## 🐳 Running with Docker Compose

### 1. Build and start

```bash
docker compose up --build
```

---

### 2. Access the app

```text
http://localhost:8001/docs
```

Health check:

```text
http://localhost:8001/health
```

---

### 3. Run migrations (first time)

```bash
docker compose exec app alembic upgrade head
```

---

### 4. Stop the app

```bash
docker compose down
```

---

## 📦 Volume Persistence

Docker Compose uses:

```yaml
volumes:
  - .:/app
```

This ensures:

* SQLite database persists locally
* data survives container restarts
* development workflow is faster

---

## 🧪 Example Workflow

1. Start app:

```bash
docker compose up
```

2. Create user via Swagger

3. Stop app:

```bash
docker compose down
```

4. Restart:

```bash
docker compose up
```

5. Verify user still exists:

```text
GET /users/
```

---

## ❤️ Health Check

```text
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

## 🔐 Security

* Passwords hashed with bcrypt
* JWT secret stored in `.env`
* Role-based authorization enforced
* Session cookies are HTTP-only

---

## ⚠️ Known Limitations

* SQLite is used (not production-grade DB)
* Session storage is in-memory
* No refresh token support yet
* No CI/CD pipeline yet

---

## 🚀 Future Improvements

* PostgreSQL integration
* Redis for session storage
* Refresh token implementation
* Deployment (Render / Railway / AWS)
* CI/CD pipeline
* Automated tests

---

## 🧠 Key Learnings

* REST API design and HTTP methods
* Authentication vs Authorization
* Stateless vs Stateful systems
* Schema validation with Pydantic
* ORM usage with SQLAlchemy
* Database migrations with Alembic
* Environment-based configuration
* Docker containerization
* Docker Compose orchestration
* Volume-based persistence

---

## 👨‍💻 Author

Backend engineering learning project built with a focus on real-world systems, production mindset, and hands-on implementation.
