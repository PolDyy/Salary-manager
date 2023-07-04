from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./main/app/test/test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
