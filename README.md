# YaMDB

![Foodgram_workflow](https://github.com/comsomolec/yamdb_final/actions/workflows/main.yml/badge.svg)

* Проект доступен по адресу: http://158.160.101.218

* Полная документация доступна по адресу: http://158.160.101.218/redoc/

## Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории:
«Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен (например, можно добавить категорию
«Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения
«Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая
сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению
рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя
оценка произведения.

## Технологии
- Python 3.9
- Django 3.2
- DRF 3.12.4
- JWT
- Docker
- Nginx
- Gunicorn

## Над проектом работали Владислав Ярёменко (Categories/Genres/Titles), Айк Саргсян (Auth/Users), Сергей Сабирзянов (Review/Comments)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:haiksarg/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3.7 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python3.7 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip3.7 install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Запуск на удаленном сервере

Установить Docker и Docker-compose:

```
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io
sudo apt install docker-compose -y
```
Клонировать репозиторий:

```
git clone git@github.com:haiksarg/infra_sp2.git
cd infra_sp2
```

Развернуть проект:

```
cd infra
docker-compose up -d --build
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Сбор статики:

```
docker-compose exec web python manage.py collectstatic --no-input
```

Проверка:

```
Приложение успешно разворачивается и становится доступным по адресу http://localhost/admin/.
```

## Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладет правами администратора (admin)

## Примеры работы с учетными записями через запросы к API
Подробная документация доступна по адресу `http://127.0.0.1:8000/redoc/`

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится.

### Регистрация нового пользователя
Получить код подтверждения на переданный email. 

- Права доступа: Доступно без токена.
- Использовать имя 'me' в качестве username запрещено. 
- Поля email и username должны быть уникальными.
- Регистрация нового пользователя:

Method:POST `/api/v1/auth/signup/`
```
{
 "email": "string",
 "username": "string"
}
```

### Получение JWT-токена:
Method:POST `/api/v1/auth/token/`
```

{
 "username": "string",
 "confirmation_code": "string"
}
```

### Получение списка всех пользователей.
- Права доступа: Администратор

Method:GET `/api/v1/users/`

### Добавление пользователя:
- Права доступа: Администратор
- Поля email и username должны быть уникальными.

Method:POST `/api/v1/users/`
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
### Получение пользователя по username:
- Права доступа: Администратор

Method:GET `/api/v1/users/{username}/`

### Изменение данных пользователя по username:
- Права доступа: Администратор

Method:PATCH `/api/v1/users/{username}/`
```
{
 "username": "string",
 "email": "user@example.com",
 "first_name": "string",
 "last_name": "string",
 "bio": "string",
 "role": "user"
}
```

### Удаление пользователя по username:
- Права доступа: Администратор

Method: DELETE `/api/v1/users/{username}/`

### Получение данных своей учетной записи:
- Права доступа: Любой авторизованный пользователь

Method:GET `/api/v1/users/me/`

### Изменение данных своей учетной записи:
- Права доступа: Любой авторизованный пользователь

Method:PATCH `/api/v1/users/me/`

## Примеры работы с моделями Categories(Категории)

### Получить список всех категорий:
- Права доступа: Любой авторизованный пользователь

Method:GET `/api/v1/categories/`

### Добавление новой категории:
- Права доступа: Администратор

Method:POST `/api/v1/categories/`

### Удаление категории:
- Права доступа: Администратор

Method:DELETE `/api/v1/categories/{slug}/`

## Примеры работы с моделями Genres(Жанры)
### Получение списка всех жанров:
- Права доступа: Любой пользователь

Method:GET `/api/v1/genres/`

### Добавление жанра:
- Права доступа: Администратор

Method:POST `/api/v1/genres/`

### Удаление жанра:
- Права доступа: Администратор

Method:DELETE `/api/v1/genres{slug}/`

## Примеры работы с моделями Titles(Произведения)

### Получение списка всех произведений:
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/`

### Добавление произведения:
- Права доступа: Администратор

Method:POST `/api/v1/titles/`

### Получение информации о произведении:
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{titles_id}/`

### Частичное обновление информации о произведении:
- Права доступа: Администратор

Method:PATCH `/api/v1/titles/{titles_id}/`

### Удаление произведения:
- Права доступа: Администратор

Method:DELETE `/api/v1/titles/{titles_id}/`

## Примеры работы с моделями Reviews(Отзывы)

### Получения списка всех отзывов
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/`

### Создание нового отзыва
- Права доступа: Любой авторизованный пользователь

Method:POST `/api/v1/titles/{title_id}/reviews/`
```
{
  "text": "string",
  "score": 1
}
```

### Получение пользователя по ID
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/{review_id}/`
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
### Частичное обновление отзыва по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:PATCH `/api/v1/titles/{title_id}/reviews/{review_id}/`
```
{
  "text": "string",
  "score": 1
}
```
### Удаление отзыва по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:DELETE `/api/v1/titles/{title_id}/reviews/{review_id}/`

## Примеры работы с моделями Comments(Комментарии)

### Получения списка всех комментариев к отзыву
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`

### Добавление комментария к отзыву
- Права доступа: Любой авторизованный пользователь

Method:POST `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`
```
{
  "text": "string"
}
```

### Добавление комментария к отзыву по ID
- Права доступа: Любой пользователь

Method:GET `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`

### Частичное обновление комментария к отзыву по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:PATCH `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
```
{
  "text": "string"
}
```
### Удаление комментария к отзыву по ID
- Права доступа: Автор отзыва, модератор или администратор

Method:DELETE `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
