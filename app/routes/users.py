from fastapi import APIRouter, Response, status, Depends, HTTPException, Query

from app.schemas.user import UserCreate, UserReplace, UserUpdate, UserResponse, PaginatedUserResponse
from app.services.user_service import UserService
from app.api.deps.user_dependencies import get_user_service

from app.dependencies.auth import require_authenticated_user, require_owner_or_admin, require_admin

from typing import Optional

router = APIRouter()


@router.get("/", response_model=PaginatedUserResponse)
def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    role: Optional[str] = None,
    email: Optional[str] = None,
    search: Optional[str] = None,
    service: UserService = Depends(get_user_service),
):
    return service.get_users_paginated(
        page=page,
        size=size,
        role=role,
        email=email,
        search=search,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int, 
    current_user=Depends(require_authenticated_user),
    service: UserService = Depends(get_user_service)):

    require_owner_or_admin(current_user, user_id)

    return service.get_user(user_id)


@router.post("/", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserReplace,
    current_user=Depends(require_authenticated_user),
    service: UserService = Depends(get_user_service),
):
    if user_id != user_update.id:
        raise HTTPException(
            status_code=400,
            detail="Path user_id must match body id",
        )

    require_owner_or_admin(current_user, user_id)

    return service.replace_user(user_id, user_update)


@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(
    user_id: int,
    user_update: UserUpdate,
    current_user=Depends(require_authenticated_user),
    service: UserService = Depends(get_user_service),
):
    require_owner_or_admin(current_user, user_id)

    return service.patch_user(user_id, user_update)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int, 
    current_user=Depends(require_admin),
    service: UserService = Depends(get_user_service),
    ):
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