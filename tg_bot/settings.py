from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class TgBot:
    bot_token: str
    admins: List[int]
    use_redis: bool


@dataclass
class DbConfig:
    user: str
    password: str
    host: str
    database: str
    port: int


@dataclass
class Misk:
    other_params: str = None


@dataclass
class Settings:
    tg_bot: TgBot
    db: DbConfig
    misc: Misk


def load_settings(path: str = None):
    env = Env()
    env.read_env(path)

    return Settings(
        TgBot(
            bot_token=env.str('BOT_TOKEN'),
            use_redis=env.str('USE_REDIS'),
            admins=list(map(int, env.list('ADMINS')))
        ),
        DbConfig(
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            database=env.str('DB_NAME'),
            port=env.int('DB_PORT')
        ),
        Misk()
    )


def load_db_cnf(path: str = None):
    env = Env()
    env.read_env(path)

    return DbConfig(
        user=env.str('DB_USER'),
        password=env.str('DB_PASS'),
        host=env.str('DB_HOST'),
        database=env.str('DB_NAME'),
        port=env.int('DB_PORT')
    )
