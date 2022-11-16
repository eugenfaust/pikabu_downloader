from sqlalchemy import Column, BigInteger, String, Boolean, DateTime

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    status = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    last_action = Column(DateTime(timezone=True))
    username = Column(String(50))
    full_name = Column(String(50))
    created = Column(DateTime(timezone=True))