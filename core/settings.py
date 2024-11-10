import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    ai_token: str

@dataclass
class Project:
    name: str
    description: str
    link: str
    link_text: str

@dataclass
class Database:
    host: str
    port: int
    user: str
    password: str
    database: str

@dataclass
class Settings:
    bots: Bots
    project: Project
    database: Database
    memory_count: int = 2

def get_settings():
    load_dotenv()

    return Settings(
        bots=Bots(
            bot_token=os.getenv("BEE_TOKEN"),
            admin_id=int(os.getenv("ADMIN_ID")),
            ai_token=os.getenv("AI_TOKEN")
        ),
        database=Database(
            host=os.getenv("DATABASE_HOST"),
            port=int(os.getenv("DATABASE_PORT")),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME")
        ),
        project=Project(
            name="Beehive",
            description="AI bots with context in Telegram",
            link="https://github.com/devnsko/ai-bee",
            link_text="GitHub"
        )
    )


settings = get_settings()
