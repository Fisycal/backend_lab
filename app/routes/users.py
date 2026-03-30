from fastapi import APIRouter, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserReplace, UserUpdate, UserResponse
from app.utils.password import hash_password

router = APIRouter()


# Route 1: GET all users
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# Route 2: GET one user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Route 3: POST create user
@router.post("/", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_id = db.query(User).filter(User.id == user.id).first()
    if existing_id:
        raise HTTPException(status_code=400, detail="User ID already exists")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        id=user.id,
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# Route 4: PUT replace user completely
@router.put("/{user_id}", response_model=UserResponse)
def replace_user(user_id: int, updated_user: UserReplace, db: Session = Depends(get_db)):
    if updated_user.id != user_id:
        raise HTTPException(status_code=400, detail="Path user_id must match body id")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email_owner = db.query(User).filter(User.email == updated_user.email, User.id != user_id).first()
    if email_owner:
        raise HTTPException(status_code=400, detail="Email already exists")

    user.name = updated_user.name
    user.email = updated_user.email

    db.commit()
    db.refresh(user)
    return user


# Route 5: PATCH partially update user
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updates: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = updates.model_dump(exclude_unset=True)

    if "email" in update_data:
        email_owner = db.query(User).filter(User.email == update_data["email"], User.id != user_id).first()
        if email_owner:
            raise HTTPException(status_code=400, detail="Email already exists")

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# Route 6: DELETE user
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Route 7a: HEAD for all users
@router.head("/")
def get_all_users_headers(db: Session = Depends(get_db)):
    users_exist = db.query(User.id).first()
    if users_exist:
        return Response(status_code=200)
    return Response(status_code=200)


# Route 7b: HEAD for a user
@router.head("/{user_id}")
def get_user_headers(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User.id).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=200)


# Route 8a: OPTIONS for all users
@router.options("/")
def get_users_options():
    return Response(
        headers={"Allow": "GET, POST, HEAD, OPTIONS"},
        status_code=200
    )


# Route 8b: OPTIONS for a user
@router.options("/{user_id}")
def get_user_options(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User.id).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(
        headers={"Allow": "GET, PUT, PATCH, DELETE, HEAD, OPTIONS"},
        status_code=200
    )