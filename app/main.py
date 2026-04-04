from fastapi import FastAPI, Depends
from app.routes import users, auth
from sqlalchemy.orm import Session
from app.db.database import Base, engine, get_db
from app.db import models

app = FastAPI(
    title="Backend Concepts Lab",
    version="1.0.0",
    description="Backend Concepts Lab"
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {
        "message": "Backend Concepts Lab is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def heath_check(db: Session = Depends(get_db)):
    return {
        "status": "ok",
        "service": "backend-concepts-lab"
        
    }
