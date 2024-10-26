from sqlalchemy import ForeignKey, String, BigInteger, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import List, Optional
from datetime import datetime, timezone

# PostgreSQL connection string
engine = create_async_engine(
    'postgresql+asyncpg://postgres.xfbilzbrfqicrsiedwzo:d!S!A5-4m?JaUV*@aws-0-eu-central-1.pooler.supabase.com:6543/postgres',
    echo=True,
    # "d!S!A5-4m?JaUV*"
)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

# User model
class User(TimestampMixin, Base):
    __tablename__ = 'beehive-user'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    number: Mapped[str] = mapped_column(String(20), nullable=True)
    
    own_bots: Mapped[List["Bot"]] = relationship(back_populates="own_bots")
    bot_id: Mapped[Optional[int]] = mapped_column(ForeignKey("beehive-bot"))
    bot: Mapped[Optional["Bot"]] = relationship(back_populates="bot")
    chat_history: Mapped[List["ChatHistory"]] = relationship(back_populates="chat_history")

# BotConfig model
class Bot(TimestampMixin, Base):
    __tablename__ = 'beehive-bot'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    context: Mapped[str] = mapped_column(String)
    public: Mapped[bool] = mapped_column(Boolean, default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("beehive-user.id"))
    author: Mapped["User"] = relationship(back_populates="auhor")
    users: Mapped[List["User"]] = relationship(back_populates="users")

# History model
class ChatHistory(TimestampMixin, Base):
    __tablename__ = 'beehive-chat-history'

    id: Mapped[int] = mapped_column(primary_key=True)
    u_id: Mapped[int] = mapped_column(ForeignKey('beehive-user.id'))
    role: Mapped[str] = mapped_column(String(30))
    message_id: Mapped[int] = mapped_column()
    content: Mapped[str] = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
