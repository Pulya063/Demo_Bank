from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.enums import Currency, Category
from app.main import app
from app.db.database import Base, get_db

SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

TestingSession = sessionmaker(autocommit = False, autoflush=False, bind=engine)

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_account_data():
    return {
        "name": "Ivan",
        "surname": "Petrenko",
        "birth_date": "2000-01-15",
        "transactions": []
    }


@pytest.fixture
def sample_transaction_data():
    return {
        "value": 500.0,
        "currency": Currency.USD.value,
        "date": datetime.now().isoformat(),
        "name": "Salary",
        "category": Category.WORK.value
    }
