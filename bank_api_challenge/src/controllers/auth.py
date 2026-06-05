from fastapi import APIRouter


from src.schemas.auth import UserIn
from src.security import sign_jwt
from src.views.auth import UserOut

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=UserOut)
async def login(data: UserIn):
    # Aqui você implementaria a lógica para autenticar um usuário
    # Por simplicidade, vamos apenas retornar o usuário autenticado
    return sign_jwt(user_id=data.user_id)