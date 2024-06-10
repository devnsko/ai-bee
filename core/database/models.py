from sqlalchemy import ForeignKey, String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# PostgreSQL connection string
engine = create_async_engine(
    'postgresql+asyncpg://postgres:pCJbF34siSwvLgmevBL9@localhost:5433/postgres',
    echo=True,
)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# User model
class User(Base):
    __tablename__ = 'bee-users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    number: Mapped[str] = mapped_column(String(20), nullable=True)
    system_id: Mapped[int] = mapped_column() # ForeignKey('bee-system.id')


# History model
class History(Base):
    __tablename__ = 'bee-history'

    id: Mapped[int] = mapped_column(primary_key=True)
    u_id: Mapped[int] = mapped_column(ForeignKey('bee-users.id'))
    role: Mapped[str] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(String)


# SystemData (bot (bee_system)) model
class SystemData(Base):
    __tablename__ = 'bee-system'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('bee-users.id'))
    bot_name: Mapped[str] = mapped_column(String(30))
    bot_content: Mapped[str] = mapped_column(String)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    memory_count: Mapped[int] = mapped_column(BigInteger, nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
