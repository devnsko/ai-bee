from sqlalchemy import ForeignKey, String, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from openai import ChatCompletion
import enum

# PostgreSQL connection string
engine = create_async_engine(
    'postgresql+asyncpg://postgres:pCJbF34siSwvLgmevBL9@localhost:5433/postgres',
    echo=True,
)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'bee-users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    number: Mapped[str] = mapped_column(String(20), nullable=True)

#
# class History(Base):
#     __tablename__ = 'bee-history'
#
#     id: Mapped[int] = mapped_column(ForeignKey('bee-users.id'))
#     history: Mapped[ChatCompletion] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)