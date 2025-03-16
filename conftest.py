import dotenv
import requests
import pytest
import os
from dotenv import load_dotenv

from api.api_manager import ApiManager
from utils.data_generator import DataGenerator

dotenv.load_dotenv()


@pytest.fixture()
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture()
def register_user(api_manager, test_user):
    # Создаем нового пользователя
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
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
def auth_admin_user(api_manager):
    login_data = (
        os.getenv('EMAIL'),
        os.getenv('PASSWORD')
    )
    api_manager.auth_api.authenticate(login_data)


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
def create_movie(api_manager, auth_admin_user, movie_data):
    response = api_manager.movie_api.create_movie(movie_data)
    response_data = response.json()
    return response_data


@pytest.fixture()
def delete_movie(api_manager, create_movie):
    yield
    api_manager.movie_api.delete_movie(create_movie['id'])
