from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timedelta


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    salary = relationship("Salary", back_populates='user', uselist=False)


class Salary(Base):
    __tablename__ = 'salaries'

    id = Column(Integer, primary_key=True, index=True)
    salary = Column(Float, nullable=False)
    promotion = Column(Date, default=(datetime.now() + timedelta(days=30)).date())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="salary")


