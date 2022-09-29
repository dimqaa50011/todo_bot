from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core import settings

Base = declarative_base()
engine = create_async_engine(settings.db_conf.SQLALCHEMY_DATABASE_URI)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
