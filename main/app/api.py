from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from . import app, get_db
from . import crud, schemas
from .crud import get_current_user, get_user_salary
from .services.jwt.token import create_access_token
from .services.jwt.token_schemas import Token


@app.post('/signup', response_model=schemas.UserSchema)
def signup(user: schemas.UserSignUpSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким login уже существует")

    new_user = crud.create_user(db=db, user=user)
    crud.set_salary(db, salary=schemas.SalarySchema(user_id=new_user.id, salary=30000.00))
    return new_user


@app.post("/login", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.login})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/my-salary', response_model=schemas.SalarySchema)
def get_salary(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(
            status_code=400,
            detail="Необходима авторизация"
            )
    user = get_current_user(access_token, db)
    salary = get_user_salary(user.id, db)
    return salary
