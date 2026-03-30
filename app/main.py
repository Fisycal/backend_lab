from fastapi import FastAPI
from app.routes import users, auth
from sqlalchemy.orm import Session
from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend Concepts Lab",
    version="1.0.0",
    description="Milestone 1 and 2: API basics, REST, HTTP methods, status codes, and authentication."
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Backend Concepts Lab is running"}

