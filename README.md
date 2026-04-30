# Backend Concepts Lab

[![CI](https://github.com/Fisycal/backend_lab/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Fisycal/backend_lab/actions/workflows/ci.yml)
![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)

A production-style backend engineering project built with FastAPI to demonstrate core backend concepts through hands-on implementation — including REST APIs, authentication, validation, database persistence, environment configuration, migrations, containerization, deployment, production hardening, system reliability, and automated testing.

---

## Project Progression

This project was built incrementally:

* Milestone 1: API fundamentals (REST, HTTP methods)
* Milestone 2: Authentication & Authorization
* Milestone 3: Validation with Pydantic
* Milestone 4: Database integration (SQLAlchemy)
* Milestone 5: Environment config + Alembic migrations
* Milestone 6: Docker + Docker Compose + Volume persistence
* Milestone 7: Deployment (Render)
* Milestone 8: Production Hardening (Observability, Security, Reliability)
* Milestone 9: Database Reliability and Health Checks
* Milestone 10: Automated Testing and CI/CD
* Milestone 11: Service Layer, Repository Pattern & Centralized Error Handling

---

## Overview

This project demonstrates how to build a real-world backend system step-by-step — from local development to production deployment.

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
* Database reliability and health monitoring
* Automated testing and continuous integration

---

## Architecture

```
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
* SQLite (development and testing)
* PostgreSQL (production-ready)
* Alembic
* Pydantic + pydantic-settings
* Passlib (bcrypt)
* python-jose (JWT)
* Uvicorn
* Docker
* Docker Compose
* GitHub Actions (CI/CD)
* Render (deployment)

---

## Project Structure

```
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

tests/
├── conftest.py
├── test_users.py
├── test_auth.py
├── test_health.py

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

* POST /auth/login-jwt
* GET /auth/me-jwt
* GET /auth/protected-jwt
* GET /auth/admin-jwt

Uses:

Authorization: Bearer <token>

---

### Session (Stateful)

* POST /auth/login-session
* GET /auth/me-session
* POST /auth/logout-session

---

## Authorization

Role-based access control:

* admin → full access
* user → limited access

---

# Database

* SQLite (development and testing)
* SQLAlchemy ORM
* Alembic migrations
* Ready for PostgreSQL in production

---

# Milestone 9 — Database Reliability and Health Checks

## Database Reliability

* Enabled pool_pre_ping in SQLAlchemy
* Detects stale connections
* Prevents runtime failures

## Health Endpoints

GET /health/live → Application running  
GET /health/ready → App + DB ready  
GET /health → Combined health  

---

# Milestone 10 — Automated Testing and CI/CD

## Testing

* pytest framework
* FastAPI TestClient
* isolated SQLite test database
* dependency override (get_db)

## Coverage

* 48+ tests
* 92% total coverage
* near 100% route coverage

## CI/CD

* GitHub Actions runs tests on push and PR
* coverage threshold enforced
* deployment integrated with Render

---

# Known Limitations

* SQLite used for development and testing
* Session storage is in-memory
* No refresh tokens yet

---

# Future Improvements

* PostgreSQL optimization
* Redis session storage
* Refresh tokens
* Advanced monitoring
* Frontend integration

---

# Author

Backend engineering learning project focused on real-world systems, production mindset, and hands-on implementation.
