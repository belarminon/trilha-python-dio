from databases.interfaces import Record
from passlib.context import CryptContext
from src.database import database
from src.models.person import people
from src.schemas.user import UserCreate, UserUpdate
from src.exceptions import BusinessError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    async def create(self, user: UserCreate) -> Record:
        # Check if email already exists
        query = people.select().where(people.c.email == user.email)
        if await database.fetch_one(query):
            raise BusinessError("Email already registered")

        hashed_password = pwd_context.hash(user.password)
        command = people.insert().values(
            name=user.name,
            email=user.email,
            password=hashed_password,
            classification=user.classification
        )
        user_id = await database.execute(command)
        return await self.get_by_id(user_id)

    async def get_by_id(self, user_id: int) -> Record | None:
        query = people.select().where(people.c.id == user_id)
        return await database.fetch_one(query)

    async def get_all(self, limit: int = 10, skip: int = 0) -> list[Record]:
        query = people.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def update(self, user_id: int, user_data: UserUpdate) -> Record:
        values = {k: v for k, v in user_data.model_dump().items() if v is not None}
        if not values:
            return await self.get_by_id(user_id)
        
        command = people.update().where(people.c.id == user_id).values(**values)
        await database.execute(command)
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        command = people.delete().where(people.c.id == user_id)
        result = await database.execute(command)
        return result > 0
