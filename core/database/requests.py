from core.database.models import async_session
from core.database.models import User, ChatHistory
from sqlalchemy import select, update, delete, desc, and_, or_

async def check_user(tg_id: int) -> bool:
    async with async_session() as session:
        async with session.begin():
            user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
            return user is not None

# Return user by telegram id or add new one if doesn't exist
async def get_user(tg_id: int) -> User: 
    async with async_session() as session:
        async with session.begin():
            # Try to fetch the user with the given tg_id
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            # If the user does not exist, create a new one
            if user is None:
                user = User(tg_id=tg_id)
                session.add(user)
                await session.flush()  # Ensure user gets an ID and is ready to be returned
    return user

# Edit context and return user
async def edit_context(tg_id: int, new_context: str) -> User:
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(User).where(User.tg_id == tg_id).values(context=new_context))

# Add /AI chat ChatHistory
async def add_chat_history(tg_id: int, role: str, content: str):
    user: User = await get_user(tg_id=tg_id)
    async with async_session() as session:
        async with session.begin():
            # Check if the content is not empty before adding to history
            if content.strip():  # Ensure content is not just whitespace
                session.add(ChatHistory(u_id=user.id, role=role, content=content))
                await session.commit()


# Get /AI chat ChatHistory
async def get_chat_history(tg_id: int, u_limit: int = 2):
    user: User = await get_user(tg_id=tg_id)
    async with async_session() as session:
        async with session.begin():
            # Ensure u_limit is a positive integer
            if u_limit <= 0:
                raise ValueError("u_limit must be a positive integer")
            histories: list[ChatHistory] = await session.scalars(
                select(ChatHistory)
                .where(ChatHistory.u_id == user.id)
                .order_by(desc(ChatHistory.id))
                .limit(2 * u_limit)
            )
            return histories


# Delete /AI chat ChatHistory
async def del_chat_history(tg_id: int):
    user: User = await get_user(tg_id=tg_id)
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(ChatHistory).where(ChatHistory.u_id == user.id))
            await session.commit()
