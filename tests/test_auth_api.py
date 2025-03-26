import json

from sqlalchemy.orm import Session

from api.api_manager import ApiManager
from db_requester.models import UserDBModel
from models.register_user_model import RegisterUserResponse
from models.user_model import TestUser


class TestAuthAPI:
    def test_register_user(self, test_user, api_manager):
        json_data = test_user.model_dump(mode='json')
        response = api_manager.auth_api.register_user(json_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    def test_auth_user(self, api_manager, register_user):
        login_data = {
            'email': register_user['email'],
            'password': register_user['password']
        }

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert response_data['accessToken'] is not None
        assert response_data['user']['email'] == register_user['email']

    def test_auth_with_invalid_password(self, test_user, register_user, api_manager):
        login_data = {
            'email': register_user['email'],
            'password': '12345678aA'
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()
        assert response_data['message'] == 'Неверный логин или пароль'

    def test_auth_with_invalid_email(self, test_user, register_user, api_manager):
        login_data = {
            'email': 'y@gmail.com',
            'password': register_user['password']
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        assert response_data['message'] == 'Неверный логин или пароль'

    def test_auth_without_body(self, api_manager):
        response = api_manager.auth_api.login_user(login_data=None, expected_status=401)
        response_data = response.json()

        assert response_data['message'] == 'Неверный логин или пароль'

    def test_register_user_db_session(self, api_manager: ApiManager, test_user: TestUser, db_session: Session):
        """
        Тест на регистрацию пользователя с проверкой в базе данных.
        """
        # выполняем запрос на регистрацию нового пользователя
        response = api_manager.auth_api.register_user(test_user.model_dump(mode='json'))
        register_user_response = RegisterUserResponse(**response.json())

        # Проверяем добавил ли сервис Auth нового пользователя в базу данных
        users_from_db = db_session.query(UserDBModel).filter(UserDBModel.id == response.json()['id'])

        # получили обьект из бзы данных и проверили что он действительно существует в единственном экземпляре
        assert users_from_db.count() == 1, "обьект не попал в базу данных"
        # Достаем первый и единственный обьект из списка полученных
        user_from_db = users_from_db.first()
        # можем осуществить проверку всех полей в базе данных например Email
        assert user_from_db.email == test_user.email, "Email не совпадает"
