from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal, engine, Base
from src.models.models import User, Account
from src.schemas.schemas import UserCreate, TransactionCreate
from src.auth import create_token
from src.services.services import deposit, withdraw, get_transactions
from exception import BusinessError
from sqlalchemy.future import select
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔌 DB Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# 🔧 Criar banco
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 👤 Cadastro
@app.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed = pwd_context.hash(user.password)

    new_user = User(username=user.username, password=hashed)
    db.add(new_user)
    await db.commit()

    # cria conta automaticamente
    account = Account(user_id=new_user.id)
    db.add(account)
    await db.commit()

    return {"msg": "Usuário criado"}


# 🔑 Login
@app.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_token({"sub": db_user.username})
    return {"access_token": token}


# 💰 Transação
@app.post("/transaction/{user_id}")
async def create_transaction(
    user_id: int,
    data: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Account).where(Account.user_id == user_id))
    account = result.scalar_one()

    if data.amount <= 0:
        raise HTTPException(400, "Valor inválido")

    if data.type == "deposit":
        await deposit(db, account, data.amount)
    elif data.type == "withdraw":
        try:
            await withdraw(db, account, data.amount)
        except BusinessError as e:
            raise HTTPException(400, str(e))
    else:
        raise HTTPException(400, "Tipo inválido")

    return {"msg": "Transação realizada"}


# 📄 Extrato
@app.get("/statement/{user_id}")
async def statement(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Account).where(Account.user_id == user_id))
    account = result.scalar_one()

    transactions = await get_transactions(db, account.id)

    return {
        "balance": account.balance,
        "transactions": transactions
    }