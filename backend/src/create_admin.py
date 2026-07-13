import asyncio
from sqlalchemy import select
from src.database import new_session
from src.users.models import UserModel
from src.users.utils import hash_password

async def create_superuser():
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    if not username or not password:
        print("Error: Username and password cannot be empty!")
        return

    hashed_password = hash_password(password)

    async with new_session() as session:
        query = await session.execute(select(UserModel).where(UserModel.username == username))
        existing_user = query.scalar_one_or_none()

        if existing_user:
            print(f"User with username '{username}' already exists!")
            return

        admin_user = UserModel(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_superuser=True
        )

        session.add(admin_user)
        await session.commit()
        print(f"Superuser '{username}' successfully created!")

if __name__ == "__main__":
    asyncio.run(create_superuser())