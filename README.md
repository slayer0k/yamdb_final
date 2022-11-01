# yamdb_final
yamdb_final
# API_YAMDB
#### Описание
Программа для получения, хранения и предоставления отзывов пользователей на различные произведения (книги, фильмы, музыка и т.д.)
#### Технологии
- Python 3.7
- Django 2.2.16
- Djangorestframework 3.12.4
#### Запуск проекта в dev-режиме
- Клонируйте репозиторий https://github.com/slayer0k/infra_sp2 с помощью команды
````
git clone
````
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt с помощью команды
````
pip install -r requirements.txt
````
- В папке с файлом manage.py выполните следующую команду
```
python3 manage.py load_reviews
```
с аргументом на выбор:

```
--all
--user
--category
--genre
--title
--titlegenre
--review
--comment
```
(для импорта информации из всех .csv файлов или же из каждого по отдельности в базу данных)
- В папке с файлом manage.py выполните команду для запуска dev-сервера:
````
python3 manage.py runserver
````
(для Linux и Mac OS)
````
python manage.py runserver
````
(для Windows)
#### Примеры запросов
###### Для неаутентифицированных пользователей:
- Регистрация пользователя: POST /api/v1/auth/signup/
- Получение JWT-токена: POST /api/v1/auth/token/
- Получение списка категорий: GET /api/v1/categories/
- Получение списка жанров: GET /api/v1/genres/
- Получение списка произведений: /api/v1/titles/
- Получение списка отзывов к произведению: /api/v1/titles/{title_id}/reviews/
- Получение списка комментариев к отзыву: /api/v1/titles/{title_id}/reviews/{review_id}/comments/
###### Только для аутентифицированных пользователей:
- Создание отзыва к произведению: POST /api/v1/titles/{title_id}/reviews/
- Создание комментария к отзыву: POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
###### Только для авторов публикации или комментария:
- Удаление отзыва: DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
- Удаление комментария: DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
###### Подробная информация по запросам - /redoc/
###### Шаблон заполнения файла .env
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=postgres
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432

##### https://github.com/slayer0k/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg

### Авторы
Сергей Чукин, Кира Изгагина, Дмитрий Самойленко
