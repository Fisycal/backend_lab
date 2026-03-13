from fastapi import FastAPI
from app.routes import users

app = FastAPI(
    title="Backend Concept Lab",
    version="1.0.0",
    description="Milestone 1: API basics, REST, HTTP methods, and status codes."
)

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Backend Concepts Lab is running"}