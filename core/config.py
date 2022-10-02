from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator

BASE_DIR = Path(__file__).parent.parent


class BaseEnvFile(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


class DBConfig(BaseEnvFile):
    DB_PASS: str
    DB_USER: str
    DB_HOST: str
    DB_NAME: str

    SQLALCHEMY_DATABASE_URI: PostgresDsn = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]):
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DB_USER"),
            password=values.get("DB_PASS"),
            host=values.get("DB_HOST"),
            path=f'/{values.get("DB_NAME") or ""}',
        )


class SchedulerDB(BaseEnvFile):
    SCHEDULER_HOST: str
    SCHEDULER_PORT: int


class BotConfig(BaseEnvFile):
    ADMINS: str
    BOT_TOKEN: str
    USE_REDIS: bool


class Settings(BaseEnvFile):
    db_conf: DBConfig = DBConfig()
    scheduler_db: SchedulerDB = SchedulerDB()
    bot_config: BotConfig = BotConfig()


settings = Settings()
