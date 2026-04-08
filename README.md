# Backend Concepts Lab

A production-style backend engineering project built with **FastAPI** to demonstrate core backend concepts through hands-on implementation — including REST APIs, authentication, validation, database persistence, environment configuration, migrations, containerization, deployment, and production hardening.

---

## Project Progression

This project was built incrementally:

* Milestone 1: API fundamentals (REST, HTTP methods)
* Milestone 2: Authentication & Authorization
* Milestone 3: Validation with Pydantic
* Milestone 4: Database integration (SQLAlchemy)
* Milestone 5: Environment config + Alembic migrations
* Milestone 6: Docker + Docker Compose + Volume persistence
* **Milestone 7: Deployment (Render)**
* **Milestone 8: Production Hardening (Observability, Security, Reliability)**

---

## Overview

This project demonstrates how to build a **real-world backend system** step-by-step — from local development to production deployment.

Key capabilities:

* RESTful API design
* JWT (stateless) and session (stateful) authentication
* Role-based authorization
* Input validation using Pydantic
* Persistent storage using SQLAlchemy
* Environment-based configuration using `.env`
* Database schema migrations using Alembic
* Containerization using Docker
* Multi-container orchestration using Docker Compose
* Volume-based database persistence
* Production deployment on Render
* Observability (logging, request tracing)
* Production-grade error handling
* Security hardening and middleware

---

## Architecture

```text
Client (Swagger / Postman / Frontend)
        ↓
FastAPI Routes
        ↓
Validation (Pydantic)
        ↓
Business Logic
        ↓
SQLAlchemy ORM
        ↓
Database (SQLite → PostgreSQL-ready)
        ↑
Alembic Migrations
        ↑
Docker Container
        ↑
Docker Compose (local)
        ↑
Render (production deployment)
```

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite (dev)
* PostgreSQL (production-ready)
* Alembic
* Pydantic + pydantic-settings
* Passlib (bcrypt)
* python-jose (JWT)
* Uvicorn
* Docker
* Docker Compose
* Render (deployment)

---

## Project Structure

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

# Features

## RESTful API

* Full CRUD for users
* Supports GET, POST, PUT, PATCH, DELETE
* Includes HEAD and OPTIONS methods

---

## Authentication

### JWT (Stateless)

* `POST /auth/login-jwt`
* `GET /auth/me-jwt`
* `GET /auth/admin-jwt`

Uses:

```
Authorization: Bearer <token>
```

---

### Session (Stateful)

* `POST /auth/login-session`
* `GET /auth/me-session`
* `POST /auth/logout-session`

---

## Authorization

Role-based access control:

* `admin` → full access
* `user` → limited access

---

# Database

* SQLite (development)
* SQLAlchemy ORM
* Alembic migrations
* Ready for PostgreSQL in production

---

# Database Migrations (Alembic)

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

# Environment Configuration

`.env` controls runtime settings:

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Additional production settings:

```env
APP_NAME=Backend Concepts Lab
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:3000"]
ALLOWED_HOSTS=["*"]
DOCS_ENABLED=true
```

Never commit `.env` to GitHub.

---

# Running with Docker Compose

### 1. Build and start

```bash
docker compose up --build
```

---

### 2. Access the app

```
http://localhost:8001/docs
```

Health check:

```
http://localhost:8001/health
```

---

### 3. Run migrations

```bash
docker compose exec app alembic upgrade head
```

---

### 4. Stop

```bash
docker compose down
```

---

# Volume Persistence

Ensures:

* database persists locally
* data survives container restarts
* faster development workflow

---

# Milestone 7 — Deployment

The backend is deployed to production using Render.

### Live API

* Root: `/`
* Health: `/health`
* Docs: `/docs`

### Deployment Features

* Public API access
* Environment variables managed in Render
* Production-ready configuration
* Database connection via environment

---

# Milestone 8 — Production Hardening

This milestone upgrades the backend to **production-grade reliability and observability**.

---

## Structured Logging

* Standardized log format
* Endpoint-level logging
* Database health logs
* Clear logs in Render

---

## Request Tracing

Each request includes:

* Unique Request ID
* Execution time tracking

Response headers:

```
X-Request-ID
X-Process-Time-ms
```

---

## Global Error Handling

Unified error responses:

```json
{
  "status": "error",
  "error": {
    "type": "validation_error",
    "message": "Request validation failed"
  }
}
```

---

## Startup Validation

Application validates critical config at startup:

* DATABASE_URL
* SECRET_KEY
* ENVIRONMENT

Fails fast if missing.

---

## CORS Configuration

* Controlled via `ALLOWED_ORIGINS`
* Supports frontend integration
* Secure defaults

---

## Security Hardening

### Response Headers

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
```

---

### Health Endpoint Protection

```
Cache-Control: no-store
```

---

### Docs Control

Swagger/ReDoc configurable:

```env
DOCS_ENABLED=false
```

---

## Proxy & Host Hardening

* Trusted host validation
* Proxy-aware request handling
* Accurate client IP detection

---

# Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

# Known Limitations

* SQLite used for development
* Session storage is in-memory
* No refresh tokens yet
* No CI/CD pipeline yet

---

# Future Improvements

* PostgreSQL production integration
* Redis for session storage
* Refresh token system
* CI/CD pipeline
* Automated testing
* Frontend integration

---

# Key Learnings

* REST API design
* Authentication vs Authorization
* Stateless vs Stateful systems
* ORM with SQLAlchemy
* Alembic migrations
* Docker & Compose
* Deployment to production
* Logging and observability
* Error handling patterns
* Security best practices

---

# Author

Backend engineering learning project focused on **real-world systems, production mindset, and hands-on implementation**.
