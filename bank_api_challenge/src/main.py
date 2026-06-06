from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import account, auth, transaction, user
from src.database import database, engine, metadata
from src.exceptions import AccountNotFoundError, BusinessError


async def seed_data():
    """Helper to seed initial users and transactions if the database is empty."""
    from src.services.user import UserService
    from src.services.account import AccountService
    from src.services.transaction import TransactionService
    from src.schemas.user import UserCreate
    from src.schemas.account import AccountIn
    from src.schemas.transaction import TransactionIn
    from src.models.person import PersonType, PersonDocument
    from src.models.transaction import TransactionType

    user_service = UserService()
    acc_service = AccountService()
    tx_service = TransactionService()

    if not await user_service.get_all(limit=1):
        # 1. Register Individual User
        u1 = await user_service.create(UserCreate(
            name="Joao Silva", 
            username="joaosilva", 
            email="joao@individual.com.br", 
            password="password123", 
            classification=PersonType.INDIVIDUAL,
            document="12345678901", 
            document_type=PersonDocument.CPF
        ))
        a1 = await acc_service.create(AccountIn(user_id=u1['id'], balance=0))
        await tx_service.create(TransactionIn(account_id=a1['id'], amount=1000.0, type=TransactionType.DEPOSIT))
        await tx_service.create(TransactionIn(account_id=a1['id'], amount=200.0, type=TransactionType.WITHDRAWAL))

        # 2. Register Company User
        u2 = await user_service.create(UserCreate(
            name="Tech Solutions LTDA", 
            username="techsolutions", 
            email="contact@techcorp.com.br", 
            password="companypass", 
            classification=PersonType.COMPANY,
            document="12345678000199", 
            document_type=PersonDocument.CNPJ
        ))
        a2 = await acc_service.create(AccountIn(user_id=u2['id'], balance=0))
        await tx_service.create(TransactionIn(account_id=a2['id'], amount=50000.0, type=TransactionType.DEPOSIT))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    metadata.create_all(bind=engine)
    await database.connect()
    await seed_data()
    yield
    await database.disconnect()


tags_metadata = [
    {
        "name": "accounts",
        "description": "Gerenciamento de contas e transações"
    },
    {
        "name": "auth",
        "description": "Autenticação de usuários"
    },
    {
        "name": "transactions",
        "description": "Gerenciamento de transações"
    },
    {
        "name": "users",
        "description": "Gerenciamento de dados cadastrais de usuários"
    },
]


app = FastAPI(
    title="API de Gerenciamento Financeiro",
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    summary="Microservice for financial operations, authentication, and user management.",
    description="""
    ### Documentation for the Financial Management API
    This API handles multi-type user registration (Individual/Company), 
    secure authentication, and transactional flows.
    
    - **Auth**: Token generation for secure access.
    - **Users**: Profile management.
    - **Accounts**: Balance tracking.
    - **Transactions**: History and deposits/withdrawals.
    """,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(account.router, tags=["accounts"])
app.include_router(transaction.router, tags=["transactions"])
app.include_router(auth.router, tags=["auth"])
app.include_router(user.router, tags=["users"])


@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )   
    
@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)}
    )
