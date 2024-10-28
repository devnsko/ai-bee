from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from core.settings import settings

db = settings.database

# PostgreSQL connection string
engine = create_async_engine(
    f'postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}',
    echo=True,
    connect_args={"statement_cache_size": 0}  # Disable statement caching
)

async_session = async_sessionmaker(engine,
                                   class_=AsyncSession,
    expire_on_commit=False,)


class Base(AsyncAttrs, DeclarativeBase):
    pass

# User model
class User(Base):
    __tablename__ = 'beehive-user'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    context: Mapped[str] = mapped_column(String, nullable=True)

# History model
class ChatHistory(Base):
    __tablename__ = 'beehive-chat-history'

    id: Mapped[int] = mapped_column(primary_key=True)
    u_id: Mapped[int] = mapped_column(ForeignKey('beehive-user.id'))
    role: Mapped[str] = mapped_column(String(30))
    content: Mapped[str] = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# class TimestampMixin:
#     created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
#     updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


# # BotConfig model
# class Bot(Base):
#     __tablename__ = 'beehive-bot'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("beehive-user.id"))
    