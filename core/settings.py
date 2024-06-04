import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    ai_token: str


@dataclass
class Settings:
    bots: Bots


def get_settings():
    load_dotenv()

    return Settings(
        bots=Bots(
            bot_token=os.getenv("BEE_TOKEN"),
            admin_id=int(os.getenv("ADMIN_ID")),
            ai_token=os.getenv("AI_TOKEN")
        )
    )


settings = get_settings()
