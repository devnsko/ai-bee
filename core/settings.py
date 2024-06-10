import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    ai_token: str

@dataclass
class System:
    bot_name: str
    bot_content: str
    memory_count: int = 2

@dataclass
class Settings:
    bots: Bots
    basic: System


def get_settings():
    load_dotenv()

    return Settings(
        bots=Bots(
            bot_token=os.getenv("BEE_TOKEN"),
            admin_id=int(os.getenv("ADMIN_ID")),
            ai_token=os.getenv("AI_TOKEN")
        ),
        basic=System(
            bot_name=os.getenv("BEE_BASIC_NAME"),
            bot_content=os.getenv("BEE_BASIC_CONTENT"),
            memory_count=int(os.getenv("BEE_BASIC_MEMORY_COUNT"))
        )
    )


settings = get_settings()
