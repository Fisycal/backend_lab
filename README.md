# Backend Concepts Lab

[![CI](https://github.com/Fisycal/backend_lab/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Fisycal/backend_lab/actions/workflows/ci.yml)
![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)

A production-grade backend system built with FastAPI, demonstrating
real-world API design, authentication, authorization, scalability, and
deployment practices.

This project was developed incrementally to simulate how backend systems
evolve in production environments.

------------------------------------------------------------------------

## Live API

Base URL: https://backend-concepts-lab.onrender.com

Swagger Documentation: https://backend-concepts-lab.onrender.com/docs

Example request:

GET /users/?page=1&size=5

------------------------------------------------------------------------

## What This Project Demonstrates

-   Secure authentication (JWT + sessions)
-   Role-based access control (RBAC)
-   Resource ownership enforcement
-   Clean architecture (routes → services → repositories)
-   Pagination, filtering, and search
-   Database migrations and reliability
-   Containerized deployment
-   Automated testing and CI/CD

------------------------------------------------------------------------

## Architecture

Client → Routes → Dependencies → Services → Repositories → Database

------------------------------------------------------------------------

## Tech Stack

-   Python
-   FastAPI
-   SQLAlchemy
-   PostgreSQL-ready
-   Alembic
-   Pydantic
-   Passlib (bcrypt)
-   python-jose (JWT)
-   Docker
-   GitHub Actions
-   Render

------------------------------------------------------------------------

## Testing

-   Pytest
-   FastAPI TestClient
-   High coverage

------------------------------------------------------------------------

## Author

Michael Ogunsanya
Industrial Engineer → Backend & AI Systems Builder
