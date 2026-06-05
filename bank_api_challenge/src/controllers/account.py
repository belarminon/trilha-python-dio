from fastapi import APIRouter, Depends, status

from src.schemas.account import AccountIn
from src.security import login_required
from src.services.account import AccountService
from src.services.transaction import TransactionService
from src.schemas.transaction import Transaction
from src.views.account import AccountOut, TransactionOut



router = APIRouter(prefix="/accounts", dependencies=[Depends(login_required)])

account_service = AccountService()
transaction_service = TransactionService()

@router.get("/", response_model=list[AccountOut])
async def read_accounts(limit: int, skip: int = 0):
    return await account_service.read_all(limit=limit, skip=skip)

@router.post("/", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
async def create_account(account_in: AccountIn):
    return await account_service.create(account_in)

@router.get("/{account_id}/transactions", response_model=list[TransactionOut])
async def read_transactions(account_id: int, limit: int, skip: int = 0):
    return await transaction_service.read_all(account_id=account_id, limit=limit, skip=skip)