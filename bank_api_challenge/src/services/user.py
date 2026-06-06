import sqlalchemy as sa
from databases.interfaces import Record
from passlib.context import CryptContext
from src.database import database
from src.models.person import people
from src.models.user import users
from src.schemas.user import UserCreate, UserUpdate
from src.exceptions import BusinessError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    async def create(self, user: UserCreate) -> Record:
        # Check if email or username already exists
        query = users.select().where((users.c.email == user.email) | (users.c.username == user.username))
        if await database.fetch_one(query):
            raise BusinessError("User with this email or username already registered")

        # 1. Create Person (Physical/Legal Data)
        person_command = people.insert().values(
            name=user.name,
            document=user.document,
            document_type=user.document_type,
            classification=user.classification
        )
        person_id = await database.execute(person_command)

        # 2. Create User (Credentials) linked to Person
        hashed_password = pwd_context.hash(user.password)
        user_command = users.insert().values(
            username=user.username,
            email=user.email,
            password=hashed_password,
            person_id=person_id
        )
        user_id = await database.execute(user_command)
        return await self.get_by_id(user_id)

    async def get_by_id(self, user_id: int) -> Record | None:
        query = sa.select(
            users.c.id, users.c.username, users.c.email, users.c.person_id, users.c.created_at,
            people.c.name, people.c.classification, people.c.document, people.c.document_type
        ).select_from(users.join(people)).where(users.c.id == user_id)
        return await database.fetch_one(query)

    async def get_all(self, limit: int = 10, skip: int = 0) -> list[Record]:
        query = users.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def update(self, user_id: int, user_data: UserUpdate) -> Record:
        user_record = await self.get_by_id(user_id)
        if not user_record:
            raise BusinessError("User not found")

        update_data = user_data.model_dump(exclude_unset=True)
        if not update_data:
            return user_record

        # Split values between linked tables
        people_fields = {"name", "classification"}
        user_fields = {"email"}

        people_updates = {k: v for k, v in update_data.items() if k in people_fields}
        user_updates = {k: v for k, v in update_data.items() if k in user_fields}

        if people_updates:
            command = people.update().where(people.c.id == user_record.person_id).values(**people_updates)
            await database.execute(command)

        if user_updates:
            command = users.update().where(users.c.id == user_id).values(**user_updates)
            await database.execute(command)

        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        user_record = await self.get_by_id(user_id)
        if not user_record:
            return False

        # Delete the user credentials record
        user_command = users.delete().where(users.c.id == user_id)
        await database.execute(user_command)

        # Delete the associated personal data record
        person_command = people.delete().where(people.c.id == user_record.person_id)
        result = await database.execute(person_command)

        return result > 0
