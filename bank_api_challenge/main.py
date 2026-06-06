from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError



@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
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
]


app = FastAPI(
    
    title="API de Gerenciamento Financeiro",
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    summary="Microservice to maintain withdrawals and deposits operations, with authentication and account management features.",
    description="""
    API para gerenciamento de contas e transações financeiras
     
        ## Account Endpoints
        
        - `GET /accounts`: Listar contas com paginação
        - `POST /accounts`: Criar uma nova conta
        - `GET /accounts/{account_id}/transactions`: Listar transações de uma conta específica com paginação
        
        ## Authentication Endpoints
        
        - `POST /auth/login`: Realizar login e obter um token de acesso
        
        ## Transaction Endpoints
        
        - `POST /transactions`: Realizar uma transação (depósito ou saque)
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

app.include_router(account.router, tags=["account"])
app.include_router(transaction.router, tags=["transaction"])
app.include_router(auth.router, tags=["auth"])


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



















# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# # 🔌 DB Dependency
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session


# # 🔧 Criar banco
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# # 👤 Cadastro
# @app.post("/register")
# async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     hashed = pwd_context.hash(user.password)

#     new_user = User(username=user.username, password=hashed)
#     db.add(new_user)
#     await db.commit()

#     # cria conta automaticamente
#     account = Account(user_id=new_user.id)
#     db.add(account)
#     await db.commit()

#     return {"msg": "Usuário criado"}


# # 🔑 Login
# @app.post("/login")
# async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(User).where(User.username == user.username))
#     db_user = result.scalar_one_or_none()

#     if not db_user or not pwd_context.verify(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Credenciais inválidas")

#     token = create_token({"sub": db_user.username})
#     return {"access_token": token}


# # 💰 Transação
# @app.post("/transaction/{user_id}")
# async def create_transaction(
#     user_id: int,
#     data: TransactionCreate,
#     db: AsyncSession = Depends(get_db)
# ):
#     result = await db.execute(select(Account).where(Account.user_id == user_id))
#     account = result.scalar_one()

#     if data.amount <= 0:
#         raise HTTPException(400, "Valor inválido")

#     if data.type == "deposit":
#         await deposit(db, account, data.amount)
#     elif data.type == "withdraw":
#         try:
#             await withdraw(db, account, data.amount)
#         except BusinessError as e:
#             raise HTTPException(400, str(e))
#     else:
#         raise HTTPException(400, "Tipo inválido")

#     return {"msg": "Transação realizada"}


# # 📄 Extrato
# @app.get("/statement/{user_id}")
# async def statement(user_id: int, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Account).where(Account.user_id == user_id))
#     account = result.scalar_one()

#     transactions = await get_transactions(db, account.id)

#     return {
#         "balance": account.balance,
#         "transactions": transactions
#     }