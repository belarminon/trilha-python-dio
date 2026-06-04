from sqlalchemy.future import select
from models import Account, Transaction

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
        raise Exception("Saldo insuficiente")

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