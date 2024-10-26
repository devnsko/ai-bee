from core.database.models import async_session
from core.database.models import User, ChatHistory, Bot
from sqlalchemy import select, update, delete, desc, and_, or_
from datetime import datetime

async def check_user(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
            return user is not None

# Return user by telegram id or add new one if doesn't exist
async def get_user(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            # Try to fetch the user with the given tg_id
            user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
            # If the user does not exist, create a new one
            if user is None:
                user = User(tg_id=tg_id)
                session.add(user)
                await session.flush()  # Ensure user gets an ID and is ready to be returned
    return user

# Add new bot
async def add_bot(tg_id: int, name: str, context: str):
    async with async_session() as session:
        async with session.begin():
            user = await get_user(tg_id=tg_id)

            new_bot = Bot(author_id=user.id, name=name, context=context, public=False)
            session.add(new_bot)
            await session.flush()
            await session.execute(update(User).where(User.id == user.id).values(bot_id=new_bot.id))


# Set bot to user
async def set_bot(tg_id: int, bot_id: int):
    async with async_session() as session:
        async with session.begin():
            user = await get_user(tg_id=tg_id)
            await session.execute(update(User).where(User.id == user.id).values(bot_id=bot_id))

#Edit bot
async def edit_current_bot(tg_id: int, new_name: str, new_context: str):
    async with async_session() as session:
        async with session.begin():
            user = await get_user(tg_id=tg_id)
            await session.execute(update(Bot).where(Bot.id == user.bot_id).values(name=new_name,context=new_context))

# Get bot  which user is using
async def get_bot(tg_id: int):
    async with async_session() as session:
        user = await get_user(tg_id=tg_id)
        bot = await session.scalar(select(Bot).where(Bot.id == user.bot_id))
        print(bot)
        return bot


# Get bot  by id
async def get_bot_by_id(bot_id: int):
    async with async_session() as session:
        bot = await session.scalar(select(Bot).where(Bot.id == bot_id))
        return bot


# Set bot  to public or private
async def switch_ispublic_bot(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            user = await get_user(tg_id=tg_id)
            bot = await session.scalar(select(Bot).where(Bot.id == user.bot_id))
            # Switch the value of is_public
            switched = not bot.is_public
            await session.execute(update(Bot).where(Bot.id == user.bot_id).values(is_public=switched))


# Get list of all bots (bots) of user and public bots
async def get_bot_list(tg_id: int):
    async with async_session() as session:
        user: User = await get_user(tg_id=tg_id)
        result = await session.scalars(select(Bot).where(or_(Bot.author_id == user.id, Bot.is_public == True)).order_by(desc(Bot.id)).limit(10))
        return result.all()


# Add /AI chat ChatHistory
async def add_bee_ChatHistory(tg_id: int, role: str, content: str):
    async with async_session() as session:
        user: User = await get_user(tg_id=tg_id)
        session.add(ChatHistory(u_id=user.id, role=role, content=content))
        await session.commit()


# Get /AI chat ChatHistory
async def get_bee_histories(tg_id: int, u_limit: int = 2):
    async with async_session() as session:
        user: User = await get_user(tg_id=tg_id)
        histories: list[ChatHistory] = await session.scalars(select(ChatHistory).where(ChatHistory.u_id == user.id).order_by(desc(ChatHistory.id)).limit(2*u_limit))
        return histories


# Delete /AI chat ChatHistory
async def del_bee_ChatHistory(tg_id: int):
    async with async_session() as session:
        user: User = await get_user(tg_id=tg_id)
        await session.execute(delete(ChatHistory).where(ChatHistory.u_id == user.id))
        await session.commit()
