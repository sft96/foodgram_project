# Foodgram
Продуктовый помощник. Данный проект позволяет зарегистрированным 
пользователям создавать рецепты, добавлять их в избранное, нужные рецепты 
отправлять в корзину, а так же подписываться на других пользователей и 
скачивать список рецептов.

### Проект доступен по следующему адресу
158.160.67.141

### Админка
- login: admin (admin@mail.ru)
- password: admin

## Как запустить
- Клонировать репозиторий
```bash
https://github.com/ShreddedCode/foodgram-project-react.git
```
- Подключиться к серверу
- Установить docker, docker-compose на сервере
```bash
sudo apt install docker.io

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
- Копировать файлы docker-compose.yml и nginx.conf на сервер
```bash
cp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml

cp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

- Cоздать .env файл на сервере и добавить в него настройки:
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

- Запустить сборку контейнеров
```bash
sudo docker compose up -d
```

- Cделать миграции, суперпользователя, собрать статику, заполнить бд 
  ингредиентами и тегами
```bash
docker compose exec backend python manage.py migrate

docker compose exec backend python manage.py createsuperuser

docker compose exec backend python manage.py collectstatic --no-input 

docker compose exec backend python manage.py load_ing_data

docker compose exec backend python manage.py load_tags_data
```

## Технологии
- Python 3.9.13
- Django 4.1.7
- Django REST framework 3.14.0
- Nginx 1.19.3
- Postgres 13.0
- Gunicorn 20.0.4

## Автор
Куличков Владислав
