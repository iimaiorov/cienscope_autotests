class TestAuthAPI:
    def test_register_user(self, test_user, api_manager):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

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

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert response_data['message'] == 'Неверный логин или пароль'

    def test_auth_with_invalid_email(self, test_user, register_user, api_manager):
        login_data = {
            'email': 'y@gmail.com',
            'password': register_user['password']
        }

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert response_data['message'] == 'Пользователь не найден'

    def test_auth_without_body(self, test_user, api_manager):
        response = api_manager.auth_api.login_user(login_data=None)
        response_data = response.json()

        assert response_data.status_code == 400
        assert response_data['message'] == 'Неверные данные'
