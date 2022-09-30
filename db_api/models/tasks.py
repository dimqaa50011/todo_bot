from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from db_api.session import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    dedline = Column(DateTime)
    complited = Column(Boolean, nullable=False, default=False)
    deleted = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
