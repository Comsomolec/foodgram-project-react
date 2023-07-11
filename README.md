# Foodgram

![Foodgram_workflow](https://github.com/comsomolec/yamdb_final/actions/workflows/main.yml/badge.svg)

* Проект доступен по адресу: http://158.160.101.218

* Полная документация доступна по адресу: http://158.160.101.218/redoc/

## Описание
Gриложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

## Технологии
- Python 3.9
- Django 3.2
- DRF 3.12.4
- JWT
- Docker
- Nginx
- Gunicorn


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Comsomolec/foodgram-project-react.git
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

## Примеры работы с учетными записями через запросы к API
Подробная документация доступна по адресу `http://127.0.0.1:8000/redoc/`

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится.

