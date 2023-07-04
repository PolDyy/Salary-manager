from . import models, schemas
from app.services.password import get_password_hash, verify_password
from config import Configs
from app.services.jwt.token_schemas import TokenData

from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_login(db: Session, login: str):
    """Возвращает пользователя по логину"""
    return db.query(models.User).filter_by(login=login).scalar()


def create_user(db: Session, user: schemas.UserSignUpSchema):
    """Создает нового пользователя"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(login=user.login,
                          password=hashed_password,
                          name=user.name,
                          surname=user.surname)
    db.add(db_user)
    db.commit()
    return db_user


def set_salary(db: Session, salary: schemas.SalarySchema):
    """Выставляет зарплату пользователю"""
    db_salary = models.Salary(salary=salary.salary, user_id=salary.user_id)
    db.add(db_salary)
    db.commit()
    return db_salary


def get_user_salary(user_id: int, db: Session):
    """Получить зарплату пользователя"""
    return db.query(models.Salary).filter_by(user_id=user_id).first()


def authenticate_user(login: str, password: str, db: Session):
    """Аутентификация пользователя"""
    user = get_user_by_login(db, login)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session):
    """Получить пользователя из токена"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Данные не валидны",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, Configs.SECRET, algorithms=[Configs.ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login)
    except JWTError:
        raise credentials_exception

    user = get_user_by_login(db, token_data.login)

    if user is None:
        raise credentials_exception
    return user
