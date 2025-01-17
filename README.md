# api_final
api final
### Описание проекта:
Данный проект представляет собой API-приложение для публикации, чтении и комментирование постов.
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AngelinaLagunova/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов:

Регистрация нового пользователя:

```
POST http://127.0.0.1:8000/api/v1/users/
Content-Type: application/json

{
    "username": "Lina",
    "password": "DjangoRest123"
}
```
Затем:

```
POST http://127.0.0.1:8000/api/v1/jwt/create/
Content-Type: application/json

{
    "username": "Lina",
    "password": "DjangoRest123"
}
```

Посмотреть все посты:
```
GET http://127.0.0.1:8000/api/v1/posts
```

Посмотреть комментарии к посту 1:
```
GET http://127.0.0.1:8000/api/v1/posts/1/comments
```

Написать пост:
```

POST http://127.0.0.1:8000/api/v1/posts/2/comments/
Content-Type: application/json
Authorization: Bearer <укажите ваш токен>

{
    "text": "some comment"   
}
```

Написать комментарий к посту 2:

```

POST http://127.0.0.1:8000/api/v1/posts/2/comments/
Content-Type: application/json
Authorization: Bearer <укажите ваш токен>

{
    "text": "some comment"   
}
```
