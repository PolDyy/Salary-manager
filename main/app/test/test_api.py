import pytest
from fastapi.testclient import TestClient
from .. import app, get_db
from .database_test import engine, TestingSessionLocal
from ..database import Base
from ..services.for_test import ForTest
from ..crud import create_user, set_salary
from ..schemas import UserSignUpSchema, SalarySchema


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()

    connection.begin()

    db = TestingSessionLocal(bind=connection)
    yield db

    db.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def add_user(db):
    user = create_user(db, UserSignUpSchema.parse_obj(ForTest.existing_user_to_sing_up))
    set_salary(db, salary=SalarySchema(user_id=user.id, salary=30000.00))


def test_create_user(client):
    response = client.post(
        "/signup",
        json=ForTest.user_to_sing_up
    )

    assert response.status_code == 200

    response = client.post(
        "/signup",
        json=ForTest.user_to_sing_up
    )
    assert response.status_code == 400
    assert response.text == '{"detail":"Пользователь с таким login уже существует"}'


def test_login_user(add_user, client):
    response = client.post('/login', data=ForTest.existing_user_for_login)
    assert response.status_code == 200


def test_get_salary(add_user, client):
    access_token = ForTest.set_access_token(client)
    response = client.get('/my-salary', headers=access_token)
    assert response.status_code == 200
    assert SalarySchema.parse_obj(response.json())
