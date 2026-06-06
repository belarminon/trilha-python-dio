from sqlalchemy.future import select
from src.models.models import Account, Transaction
from src.exceptions import BusinessError

async def deposit(db, account, amount):
    account.balance += amount

    t = Transaction(
        account_id=account.id,
        type="deposit",
        amount=amount
    )

    db.add(t)
    await db.commit()


async def withdraw(db, account, amount):
    if account.balance < amount:
        raise BusinessError("Saldo insuficiente")

    account.balance -= amount

    t = Transaction(
        account_id=account.id,
        type="withdraw",
        amount=amount
    )

    db.add(t)
    await db.commit()


async def get_transactions(db, account_id):
    result = await db.execute(
        select(Transaction).where(Transaction.account_id == account_id)
    )
    return result.scalars().all()
