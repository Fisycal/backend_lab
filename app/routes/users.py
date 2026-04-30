from fastapi import APIRouter, Response, status, Depends, HTTPException

from app.schemas.user import UserCreate, UserReplace, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.api.deps.user_dependencies import get_user_service

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user(user_id)


@router.post("/", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)


@router.put("/{user_id}", response_model=UserResponse)
def replace_user(
    user_id: int,
    updated_user: UserReplace,
    service: UserService = Depends(get_user_service)
):
    return service.replace_user(user_id, updated_user)



@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updates: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return service.update_user(user_id, updates)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.head("/")
def get_all_users_headers(service: UserService = Depends(get_user_service)):
    service.any_users_exist()
    return Response(status_code=200)


@router.head("/{user_id}")
def get_user_headers(user_id: int, service: UserService = Depends(get_user_service)):
    service.user_exists_for_head(user_id)
    return Response(status_code=200)


@router.options("/")
def get_users_options():
    return Response(
        headers={"Allow": "GET, POST, HEAD, OPTIONS"},
        status_code=200
    )


@router.options("/{user_id}")
def get_user_options(user_id: int, service: UserService = Depends(get_user_service)):
    service.user_exists_for_options(user_id)
    return Response(
        headers={"Allow": "GET, PUT, PATCH, DELETE, HEAD, OPTIONS"},
        status_code=200
    )