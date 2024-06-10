from core.database.models import async_session
from core.database.models import User, History, SystemData
from sqlalchemy import select, update, delete, desc, and_, or_
from datetime import datetime


# Add user to database
async def add_user(tg_id: int, username: str = None):
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            if not user:
                session.add(User(tg_id=tg_id, name=username))
                session.commit()
                return False
            return True


# Get user by database id
async def get_user(u_id: int):
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id == u_id))
        return user

# Get user by telegram id
async def get_user_by_tuid(tg_id: int):
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = session.add(User(tg_id=tg_id))
            await session.commit()
        return user


# Get user by username
async def get_user_by_name(username: str):
    async with async_session() as session:
        username = username.replace("@", "")
        user: User = await session.scalar(select(User).where(User.name == username))
        return user


# Add /AI chat history
async def add_bee_history(tg_id: int, role: str, content: str):
    async with async_session() as session:
        user: User = await get_user_by_tuid(tg_id=tg_id)
        session.add(History(u_id=user.id, role=role, content=content))
        await session.commit()


# Get /AI chat history
async def get_bee_histories(tg_id: int, u_limit: int = 2):
    async with async_session() as session:
        user: User = await get_user_by_tuid(tg_id=tg_id)
        histories: list[History] = await session.scalars(select(History).where(History.u_id == user.id).order_by(desc(History.id)).limit(2*u_limit))
        return histories


# Delete /AI chat history
async def del_bee_history(tg_id: int):
    async with async_session() as session:
        user: User = await get_user_by_tuid(tg_id=tg_id)
        await session.execute(delete(History).where(History.u_id == user.id))
        await session.commit()


# Add new bot (bee_system)
async def add_bee_system(tg_id: int, name: str, content: str, is_public: bool = False, memory_count: int = 2):
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_tuid(tg_id=tg_id)

            new_system = SystemData(author_id=user.id, bot_name=name, bot_content=content, is_public=is_public,
                                    memory_count=memory_count)
            session.add(new_system)
            await session.flush()
            await session.execute(update(User).where(User.id == user.id).values(system_id=new_system.id))


# Set bot (bee_system) to user
async def set_bee_system(tg_id: int, system_id: int):
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_tuid(tg_id=tg_id)
            await session.execute(update(User).where(User.id == user.id).values(system_id=system_id))

#Save new name fot bot (bee_system)
async def edit_bee_system_name(tg_id: int, new_name: str):
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_tuid(tg_id=tg_id)
            await session.execute(update(SystemData).where(SystemData.id == user.system_id).values(bot_name=new_name))


#Save new content fot bot (bee_system)
async def edit_bee_system_content(tg_id, new_content):
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_tuid(tg_id=tg_id)
            await session.execute(update(SystemData).where(SystemData.id == user.system_id).values(bot_content=new_content))


# Get bot (bee_system) which user is using
async def get_bee_system(tg_id: int):
    async with async_session() as session:
        user = await get_user_by_tuid(tg_id=tg_id)
        system = await session.scalar(select(SystemData).where(SystemData.id == user.system_id))
        print(system)
        return system


# Get bot (bee_system) by id
async def get_bee_system_by_id(system_id: int):
    async with async_session() as session:
        system = await session.scalar(select(SystemData).where(SystemData.id == system_id))
        return system


# Set bot (bee_system) to public or private
async def switch_ispublic_bee_system(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_tuid(tg_id=tg_id)
            system = await session.scalar(select(SystemData).where(SystemData.id == user.system_id))
            # Switch the value of is_public
            switched = not system.is_public
            await session.execute(update(SystemData).where(SystemData.id == user.system_id).values(is_public=switched))


# Get list of all bots (bee_systems) of user and public bots
async def get_bee_system_list(tg_id: int):
    async with async_session() as session:
        user: User = await get_user_by_tuid(tg_id=tg_id)
        result = await session.scalars(select(SystemData).where(or_(SystemData.author_id == user.id, SystemData.is_public == True)).order_by(desc(SystemData.id)).limit(10))
        return result.all()
