from typing import Optional

from pydantic import BaseModel, Field, validator
from datetime import date


class SalarySchema(BaseModel):
    user_id: int
    salary: float
    promotion: Optional[date] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    login: str = Field(min_length=2, max_length=20)
    name: str = Field(min_length=2, max_length=20)
    surname: str = Field(min_length=2, max_length=20)

    class Config:
        orm_mode = True


class UserSchema(UserBase):
    id: int
    salary: SalarySchema = None


class UserSignUpSchema(UserBase):

    password: str = Field(min_length=8)
    confirm_password: str

    @validator('confirm_password')
    def validate_password(cls, confirm_password, values):
        if values['password'] != confirm_password:
            raise ValueError("Пароли не совпадают")
        return confirm_password
