import datetime

import requests
import pytest
import os
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.api_manager import ApiManager
from constants.roles import Roles
from db_requester.models import UserDBModel
from resources.user_creds import SuperAdminCreds
from tests.test_user_api import TestUser
from utils.data_generator import DataGenerator
from entities.user import User
from models.user_model import TestUser

dotenv.load_dotenv()


@pytest.fixture()
def test_user() -> TestUser:
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )


@pytest.fixture()
def register_user(api_manager, test_user):
    # Создаем нового пользователя
    api_manager.auth_api.register_user(test_user.model_dump(mode='json'))
    registered_user = {
        "email": test_user.email,
        "password": test_user.password
    }
    return registered_user


@pytest.fixture()
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture()
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture()
def movie_data():
    random_title = DataGenerator.generate_qa_movie_title()
    random_description = DataGenerator.generate_qa_movie_description()
    return {
        "name": random_title,
        "price": 100,
        "description": random_description,
        "location": "MSK",
        "published": True,
        "genreId": 1
    }


@pytest.fixture()
def create_movie(super_admin, movie_data):
    response = super_admin.api.movie_api.create_movie(movie_data)
    response_data = response.json()
    return response_data


@pytest.fixture()
def delete_movie(super_admin, create_movie):
    yield
    super_admin.api.movie_api.delete_movie(create_movie['id'])


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.EMAIL,
        SuperAdminCreds.PASSWORD,
        list(Roles.SUPER_ADMIN.value),
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.ADMIN.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_user = test_user.model_copy(update={
        'verified': True,
        'banned': False
    })

    return updated_user.model_dump(mode='json')


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


dotenv.load_dotenv()
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('USERNAMEDB')}:{os.getenv('PASSWORDDB')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DATABASE_NAME')}")  # Создаем движок (engine) для подключения к базе данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Создаем фабрику сессий


@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных.
    После завершения теста сессия автоматически закрывается.
    """
    # Создаем новую сессию
    db_session = SessionLocal()
    # Возвращаем сессию в тест
    yield db_session
    # Закрываем сессию после завершения теста
    db_session.close()
