from core.database.models import async_session
from core.database.models import User
from sqlalchemy import select, update, delete, desc, and_, or_
from datetime import datetime


async def add_user(tg_id: int, username: str | None = None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, name=username))
            await session.commit()
            return False
        return True


async def get_user(u_id: int):
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id == u_id))
        return user


async def get_user_by_tuid(tg_id: int):
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def get_user_by_name(username: str):
    async with async_session() as session:
        username = username.replace("@", "")
        user: User = await session.scalar(select(User).where(User.name == username))
        return user
