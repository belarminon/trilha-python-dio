from fastapi import APIRouter, Depends, status

from src.schemas.transaction import TransactionIn
from src.security import login_required
from src.services.transaction import TransactionService
from src.views.transaction import TransactionOut

router = APIRouter(prefix="/transactions", dependencies=[Depends(login_required)])

transaction_service = TransactionService()

@router.post("/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_in: TransactionIn):
    return await transaction_service.create(transaction_in)