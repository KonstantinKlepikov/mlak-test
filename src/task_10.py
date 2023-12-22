"""
Напишите программу, которая делает запрос к открытому API (например, GitHub API) и выводит информацию о пользователе.
Создайте простой веб-сервер (Flask, FastAPI). Напишите эндпойнт, который добавляет результат в гугл-таблицу и эндпойнт,
который возвращает данные из гугл таблицы в виде JSON-объекта.

Run with `uvicorn src.task_10:app --reload`

Docs is available at url: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from datetime import date
import requests


EXT_ENPOINT = 'https://fakerapi.it/api/v1/books?_quantity=1'


class BookIn(BaseModel):
    """Request external api scheme

    https://fakerapi.it/api/v1/books?_quantity=1
    """
    id: int
    title: str
    author: str
    genre: str
    description: str
    isbn: int
    image: HttpUrl
    published: date
    publisher: str

    class Config:

        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "March Hare said to.",
                "author": "Jeanie Roberts",
                "genre": "Voluptatem",
                "description": "Alice said very humbly.",
                "isbn": "9798938996274",
                "image": "http://placeimg.com/480/640/any",
                "published": "1994-03-01",
                "publisher": "Et Iste"
                    }
                }


class BookOut(BaseModel):
    """Request google sheets api scheme
    """
    books: list[BookIn] = []


app = FastAPI()


@app.get("/book")
def get_book() -> None:
    q = requests.get(EXT_ENPOINT)
    if q.status_code == 200:
        b = BookIn(**q.json()["data"][0])

    # send to google sheet


@app.get("/books")
def get_books() -> BookOut:
    """"""

