from fastapi import APIRouter, HTTPException, Response, status

router = APIRouter()

users_db = [
    {"id": 1, "name": "Alice","email": "alice111@learning.com"},
    {"id": 2, "name": "Bobby","email": "bobby123@learning.com"}
]

# Route 1: GET all users
@router.get("/")
def get_users():
    return users_db

# Route 2: GET one user by ID
@router.get("/{user_id}")
def get_user(user_id: int):
    for user in users_db:
        if user["id"]  == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Route 3: POST create user
@router.post("/", status_code=201)
def create_user(user: dict):
    if "id" not in user or "name" not in user or "email" not in user:
        raise HTTPException(status_code=400, detail="id, name, and email are required")
    
    for existing_user in users_db:
        if existing_user["id"] == user["id"]:
            raise HTTPException(status_code=400, detail="User ID already exists")
    
    users_db.append(user)
    return user

# Route 4: PUT replace user completely
@router.put("/{user_id}")
def replace_user(user_id: int, updated_user: dict):
    if "id" not in updated_user or "name" not in updated_user or "email" not in updated_user:
        raise HTTPException(status_code=400, detail="id, name, and email are required")
    
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db[index] = updated_user
            return updated_user
        
    raise HTTPException(status_code=404, detail="User not found")

# Route 5: PATCH partially update user
@router.patch("/{user_id}")
def update_user(user_id: int, updates: dict):
    for user in users_db:
        if user["id"] == user_id:
            user.update(updates)
            return user
    
    raise HTTPException(status_code=404, detail="User not found")
    

# Route 6: DELETE user
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    for index, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="User not found")