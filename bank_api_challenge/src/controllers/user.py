from fastapi import APIRouter, Depends, status, HTTPException
from src.schemas.user import UserCreate, UserUpdate, UserRead
from src.services.user import UserService
from src.security import login_required

router = APIRouter(prefix="/users")
service = UserService()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return await service.create(user)

@router.get("/", response_model=list[UserRead])
async def list_users(limit: int = 10, skip: int = 0, _ = Depends(login_required)):
    return await service.get_all(limit, skip)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, _ = Depends(login_required)):
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, _ = Depends(login_required)):
    user = await service.update(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, _ = Depends(login_required)):
    success = await service.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
