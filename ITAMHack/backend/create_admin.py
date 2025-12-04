import asyncio
from backend.database import async_session
from backend.admin.utils import pwd_context
from backend.admin.services import create_admin

async def main():
    email = input("Admin email: ")
    password = input("Password: ")
    hashed_password = pwd_context.hash(password)

    async with async_session() as session:
        await create_admin(session=session, email=email, password_hash=hashed_password)

    print("Admin created!")

if __name__ == "__main__":
    asyncio.run(main())

