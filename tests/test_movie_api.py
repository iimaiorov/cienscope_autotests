from datetime import datetime, timedelta
from http.client import responses

import pytest
from sqlalchemy.orm import Session

from conftest import super_admin, common_user
from pytz import timezone

from db_requester.models import MovieDBModel
from utils.data_generator import DataGenerator


class TestMovieAPI:
    def test_get_movies(self, api_manager):
        response = api_manager.movie_api.get_movies()
        response_data = response.json()

        assert response_data is not None
        assert len(response_data['movies']) == 10

    def test_filter_by_pagesize(self, api_manager):
        response = api_manager.movie_api.get_movies(params={'page': 2, 'pageSize': 5})
        response_data = response.json()

        assert response_data is not None
        assert len(response_data['movies']) == 5
        assert response_data['pageSize'] == 5
        assert response_data['page'] == 2

    def test_get_movie_by_id(self, api_manager, create_movie, delete_movie):
        response = api_manager.movie_api.get_movie_by_id(create_movie['id'])
        response_data = response.json()

        assert response_data is not None
        assert response_data['id'] == create_movie['id']
        assert response_data['name'] == create_movie['name']
        assert response_data['description'] == create_movie['description']

    def test_create_movie(self, movie_data, super_admin):
        response = super_admin.api.movie_api.create_movie(movie_data)
        response_data = response.json()

        assert response_data is not None
        assert response_data['name'] == movie_data['name']
        assert response_data['description'] == movie_data['description']

    def test_delete_movie(self, super_admin, create_movie, db_session):
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.id == create_movie['id'])
        assert movies_from_db.count() == 1, "Фильм не попал в базу данных"
        response = super_admin.api.movie_api.delete_movie(create_movie['id'])
        response_data = response.json()
        response_get_movie = super_admin.api.movie_api.get_movie_by_id(create_movie['id'], expected_status=404)
        response_get_data = response_get_movie.json()

        assert response_data is not None
        assert response_data['id'] == create_movie['id']
        assert response_get_data['message'] == 'Фильм не найден'

    def test_create_movie_with_non_admin_user(self, movie_data, common_user):
        response = common_user.api.movie_api.create_movie(movie_data, expected_status=403)
        response_data = response.json()

        assert response_data['message'] == 'Forbidden resource'

    @pytest.mark.parametrize(
        "locations, genre_id, min_price, max_price",
        [
            (["MSK"], 1, 50, 100),
            (["SPB"], 2, 100, 300),
            (["MSK", "SPB"], 3, 200, 500),
        ]
    )
    def test_get_movies_with_filter(self, api_manager, locations, genre_id, min_price, max_price):
        params = {
            'locations': locations,
            'genreId': genre_id,
            'minPrice': min_price,
            'maxPrice': max_price
        }
        response = api_manager.movie_api.get_movies(params=params)
        response_data = response.json()
        assert response_data is not None
        for movie in response_data['movies']:
            assert movie['location'] in locations
            assert movie['genreId'] == genre_id
            assert min_price <= movie['price'] <= max_price

    @pytest.fixture
    def role(self, request):
        return request.getfixturevalue(request.param)

    @pytest.mark.parametrize("role,status", [('admin', 403), ('common_user', 403), ('super_admin', 200)],
                             indirect=['role'])
    def test_delete_movie_with_diff_role(self, role, create_movie, status):
        response = role.api.movie_api.delete_movie(create_movie['id'], expected_status=status)
        if status == 403:
            response_data = response.json()
            assert response_data['message'] == 'Forbidden resource'
        else:
            response_data = response.json()
            assert response_data['id'] == create_movie['id']
            response_get_movie = role.api.movie_api.get_movie_by_id(create_movie['id'], expected_status=404)
            response_get_data = response_get_movie.json()
            assert response_get_data['message'] == 'Фильм не найден'

    def test_create_delete_movie(self, super_admin, db_session: Session):
        # как бы выглядел SQL запрос
        """SELECT id, "name", price, description, image_url, "location", published, rating, genre_id, created_at
           FROM public.movies
           WHERE name='Test Moviej1h8qss9s5';"""

        movie_name = f"Test Movie{DataGenerator.generate_qa_movie_title()}"
        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name)
        assert movies_from_db.count() == 0, "Фильм уже существует в базе данных"

        movie_data = {
            "name": movie_name,
            "price": 100,
            "description": "Test description",
            "location": "MSK",
            "published": True,
            "genreId": 1
        }
        response = super_admin.api.movie_api.create_movie(movie_data, expected_status=201)
        response_data = response.json()

        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.id == response_data['id'])
        assert movies_from_db.count() == 1, "Фильм не попал в базу данных"

        response_delete = super_admin.api.movie_api.delete_movie(response_data['id'], expected_status=200)

        movies_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.id == response_data['id'])

        assert movies_from_db.count() == 0, "Фильм не удалился из базы данных"
