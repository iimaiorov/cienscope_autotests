from custom_requester.custom_requester import CustomRequester
from constants.constants import MOVIE_ENDPOINT


class MoviesAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru/")
        self.session = session

    def get_movie_by_id(self, movie_id=None, expected_status=200):
        """
        Получение афишы фильма по id.
        :param movie_id: ID афишы.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def get_movies(self, params=None, expected_status=200):
        """
        Получение афиш фильмов.
        :param params: Параметры запроса.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        """
        Создание новой афишы фильма.
        :param movie_data: Данные фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление афишы фильма.
        :param movie_id: ID афишы.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f'{MOVIE_ENDPOINT}/{movie_id}',
            expected_status=expected_status
        )
