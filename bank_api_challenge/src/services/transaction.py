from databases.interfaces import Record

from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError
from src.models.account import accounts
from src.models.transaction import transactions, TransactionType
from src.schemas.transaction import TransactionIn, TransactionOut

class TransactionService:
    
    async def read_all(self, account_id: int, limit: int, skip: int = 0) -> list[Record]:
        query = transactions.select().where(transactions.c.account_id == account_id).limit(limit).offset(skip)
        return await database.fetch_all(query)
    
    @database.transaction()
    
    async def create(self, transaction_in: TransactionIn) -> Record:
        query = accounts.select().where(accounts.c.id == transaction_in.account_id)
        account = await database.fetch_one(query)
        
        if not account:
            raise AccountNotFoundError("Account not found")
        
        # Validate transaction type and amount
        if transaction_in.type == TransactionType.Withdrawal and transaction_in.amount > 0:
            balance = float(account.balance) - transaction_in.amount
            if balance < 0:
                raise BusinessError("Operation not carried out due to lack of balance. Insufficient funds.")
        else:
            balance = float(account.balance) + transaction_in.amount
            
        # Create transaction entry
        transaction_id = await self.__register_transaction(transaction_in)
        # Update account balance
        await self.__update_account_balance(transaction_in.account_id, balance) 
        
        query = transactions.select().where(transactions.c.id == transaction_id)
        return await database.fetch_one(query)
    
    async def __register_transaction(self, transaction_in: TransactionIn) -> int:   
        query = transactions.insert().values(
            account_id=transaction_in.account_id,
            amount=transaction_in.amount,
            type=transaction_in.type
        )
        transaction_id = await database.execute(query)
        return transaction_id

    async def __update_account_balance(self, account_id: int, balance: float) -> None:
        query = accounts.update().where(accounts.c.id == account_id).values(balance=balance)
        await database.execute(query)





        
        
        # if transaction_in.amount <= 0:
        #     raise BusinessError("Amount must be greater than zero")

        # new_balance = account["balance"] + transaction_in.amount
        # if new_balance < 0:
        #     raise BusinessError("Insufficient funds")

        # query = """
        #     INSERT INTO transactions (account_id, amount, description)
        #     VALUES (:account_id, :amount, :description)
        #     RETURNING id, account_id, amount, description, created_at
        # """
        # values = {
        #     "account_id": transaction_in.account_id,
        #     "amount": transaction_in.amount,
        #     "description": transaction_in.description
        # }
        # record: Record = await database.fetch_one(query, values)

        # # Update account balance
        # await database.execute("UPDATE accounts SET balance = :balance WHERE id = :account_id", {"balance": new_balance, "account_id": transaction_in.account_id})

        # return TransactionOut(**record)