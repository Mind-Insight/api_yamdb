# Проект YaMDb: Отзывы пользователей на произведения

Проект YaMDb является платформой для сбора и оценки отзывов пользователей на различные произведения, такие как книги, фильмы и музыка. Этот README файл предоставляет обзор проекта и инструкции по запуску.

## Разработчики

[Vyacheslav Menyukhov](https://github.com/platsajacki) разрабатывал:
  - систему регистрации и аутентификации;
  - права доступа;
  - работу с токеном;
  - систему подтверждения через e-mail.

[Ruslan Demidov](https://github.com/Profx501) разрабатывал:
  - отзывы;
  - комментарии;
  - рейтинг произведений.

[Timofey Averchenkov](https://github.com/Mind-Insight) разрабатывал:
  - произведения;
  - категории;
  - жанры;
  - импорт данных из csv файлов.

## Технологии
- Django - веб-фреймворк для Python.
- Django REST framework (DRF) - расширение Django для создания RESTful API.
- Django-filter - фильтр запросов на основе полей модели.
- SQLite - компактная встраиваемая СУБД.

## Запуск проекта

Для запуска проекта выполните следующие шаги:

1. Установите необходимые зависимости, используя менеджер пакетов pip:
    ```bash
    git clone https://github.com/platsajacki/api_yamdb.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd api_yamdb
    ```

3. Создайте виртуальное окружение:
    - для Windows:
    ```bash
    python -m venv venv
    ```

    - для macOS и Linux:
    ```bash
    python3 -m venv venv
    ```

4. Активируйте виртуальное окружение:
    - для Windows:
    ```bash
    venv\Scripts\activate
    ```

    - для macOS и Linux:
    ```bash
    source venv/bin/activate
    ```

5. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

6. Примените миграции базы данных:
    ```bash
    python manage.py migrate
    ```

7. Создайте кэш-таблице в базе данных:
    ```bash
    python manage.py createcachetable
    ```

8. Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```

9. Теперь вы можете обращаться к API по адресу: http://127.0.0.1:8000/

## Документация API
Примеры запросов к API и их описание доступны в документации Redoc по следующему адресу: http://127.0.0.1:8000/redoc/. Здесь вы найдете подробную информацию о доступных эндпоинтах, параметрах запросов, ожидаемых данных и возможных ответах.
