from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from db_api.session import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    first_name = Column(String(30))
    last_name = Column(String(30))
    joined_date = Column(DateTime, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    deleted = Column(Boolean, nullable=False)
    tasks = relationship("Tasks", backref="users")
