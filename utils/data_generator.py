import random
import string
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_qa_movie_title():
        # Список технических существительных с указанием рода:
        # "m" — мужской, "f" — женский, "n" — средний
        nouns = [
            {"word": "баг", "gender": "m"},
            {"word": "ошибка", "gender": "f"},
            {"word": "код", "gender": "m"},
            {"word": "деплой", "gender": "m"},
            {"word": "коммит", "gender": "m"},
            {"word": "тест", "gender": "m"},
            {"word": "ревью", "gender": "n"},
            {"word": "релиз", "gender": "m"},
            {"word": "интеграция", "gender": "f"},
            {"word": "сборка", "gender": "f"},
            {"word": "инцидент", "gender": "m"},
            {"word": "фича", "gender": "f"},
            {"word": "сервис", "gender": "m"},
            {"word": "лог", "gender": "m"},
            {"word": "сессия", "gender": "f"},
            {"word": "запрос", "gender": "m"},
            {"word": "ответ", "gender": "m"},
            {"word": "событие", "gender": "n"},
            {"word": "поток", "gender": "m"},
            {"word": "процесс", "gender": "m"},
            {"word": "система", "gender": "f"},
            {"word": "платформа", "gender": "f"},
            {"word": "модуль", "gender": "m"},
            {"word": "компонент", "gender": "m"},
            {"word": "интерфейс", "gender": "m"},
            {"word": "конфигурация", "gender": "f"},
            {"word": "параметр", "gender": "m"},
            {"word": "переменная", "gender": "f"},
            {"word": "функция", "gender": "f"},
            {"word": "метод", "gender": "m"},
            {"word": "объект", "gender": "m"},
            {"word": "класс", "gender": "m"},
            {"word": "структура", "gender": "f"},
            {"word": "алгоритм", "gender": "m"},
            {"word": "библиотека", "gender": "f"},
            {"word": "фреймворк", "gender": "m"},
            {"word": "репозиторий", "gender": "m"},
            {"word": "сборка", "gender": "f"},
            {"word": "деплоймент", "gender": "m"},
            {"word": "инфраструктура", "gender": "f"}
        ]

        # Словарь прилагательных по роду (с акцентом на QA и разработку)
        adjectives = {
            "m": [
                "Баговый", "Сбойный", "Критичный", "Лаговый",
                "Глючный", "Неисправный", "Отладочный", "Отрефакторенный"
            ],
            "f": [
                "Баговая", "Сбойная", "Критичная", "Лаговая",
                "Глючная", "Неисправная", "Отладочная", "Отрефакторенная"
            ],
            "n": [
                "Баговое", "Сбойное", "Критичное", "Лаговое",
                "Глючное", "Неисправное", "Отладочное", "Отрефакторенное"
            ]
        }

        # Выбираем случайное существительное и определяем его род
        noun_choice = random.choice(nouns)
        noun_word = noun_choice["word"]
        noun_gender = noun_choice["gender"]

        # Выбираем случайное прилагательное, соответствующее роду
        adjective_choice = random.choice(adjectives[noun_gender])

        # Формируем и возвращаем название фильма
        title = f"{adjective_choice} {noun_word}"
        return title

    @staticmethod
    def generate_qa_movie_description():
        intros = [
            "Погрузитесь в мир, где каждая ошибка – повод для смеха.",
            "Добро пожаловать в реальность, где баги становятся героями.",
            "Этот фильм рассказывает о том, как тест-кейсы превращаются в захватывающие приключения.",
            "Окунитесь в вселенную, где код обретает собственный характер.",
            "Приготовьтесь к отладочной эпопее, полной неожиданных поворотов."
        ]

        middles = [
            "Здесь каждый коммит вызывает лавину неожиданных последствий.",
            "Деплой превращается в испытание, а фича – в источник иронии.",
            "Ревью становится настоящей баталией, где каждый тест – шаг к победе над хаосом.",
            "Каждая строка кода полна сюрпризов, как и жизнь разработчика.",
            "Тесты ведут к новым открытиям, а баги – к бесконечному юмору."
        ]

        ends = [
            "Смотрите, как даже ошибки становятся эпическими!",
            "Смейтесь вместе с героями до слез!",
            "Откройте для себя мир, где баги – звёзды экрана!",
            "Каждая ошибка – это новый уровень веселья!",
            "Этот фильм – настоящий тест на хорошее настроение!"
        ]

        # Формирование полного описания
        description = f"{random.choice(intros)} {random.choice(middles)} {random.choice(ends)}"

        return description
