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
    bot_context: str
    memory_count: int = 2

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
        project=Project(
            name=os.getenv("PROJECT_NAME"),
            description=os.getenv("PROJECT_DESCRIPTION"),
            link=os.getenv("PROJECT_LINK"),
            link_text=os.getenv("PROJECT_LINK_TEXT")
        ),
        database=Database(
            host=os.getenv("DATABASE_HOST"),
            port=int(os.getenv("DATABASE_PORT")),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME")
        )
    )


settings = get_settings()
