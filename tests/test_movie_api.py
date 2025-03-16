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

    def test_create_movie(self, api_manager, movie_data, auth_admin_user):
        response = api_manager.movie_api.create_movie(movie_data)
        response_data = response.json()

        assert response_data is not None
        assert response_data['name'] == movie_data['name']
        assert response_data['description'] == movie_data['description']

    def test_delete_movie(self, api_manager, create_movie):
        response = api_manager.movie_api.delete_movie(create_movie['id'])
        response_data = response.json()
        response_get_movie = api_manager.movie_api.get_movie_by_id(create_movie['id'], expected_status=404)
        response_get_data = response_get_movie.json()

        assert response_data is not None
        assert response_data['id'] == create_movie['id']
        assert response_get_data['message'] == 'Фильм не найден'
