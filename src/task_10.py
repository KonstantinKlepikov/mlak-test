"""
Напишите программу, которая делает запрос к открытому API (например, GitHub API) и выводит информацию о пользователе.
Создайте простой веб-сервер (Flask, FastAPI). Напишите эндпойнт, который добавляет результат в гугл-таблицу и эндпойнт,
который возвращает данные из гугл таблицы в виде JSON-объекта.

Для связи с google scheet использована баблиотека gspread в режиме "для юзера".
Это означает что не создавался бот, а использовался живой аккаунт.
Чтобы реализовать этот функционал, пожалуйста пройдите аутентификацию
для google по инструкции For End Users: Using OAuth Client ID:
https://docs.gspread.org/en/latest/oauth2.html#enable-api-access

Запуск приложения: `uvicorn src.task_10:app --reload`

Апи для теста руками доступно по адресу: http://127.0.0.1:8000/docs

В качестве запроса - опрашивается фейковый апи, генерирующий свойства книг:
https://fakerapi.it/api/v1/books?_quantity=1
"""
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import requests
import gspread
from gspread import Spreadsheet


EXT_ENPOINT = 'https://fakerapi.it/api/v1/books?_quantity=1'


class BookIn(BaseModel):
    """Request external api scheme
    """
    id: int
    title: str
    author: str
    genre: str
    description: str
    isbn: int
    image: str
    published: str
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

class BooksOut(BaseModel):
    """Request google sheets api scheme
    """
    books: list[BookIn] = []


def open_worksheet() -> Spreadsheet:
    """Get gspread session"""
    gc = gspread.oauth()
    return gc.open("gsheet-test")


app = FastAPI()


@app.get("/book")
def get_book(gc: Spreadsheet = Depends(open_worksheet)) -> None:
    """Get book from fake api and write it to google sheet
    """
    q = requests.get(EXT_ENPOINT)
    if q.status_code == 200:
        b_in = BookIn(**q.json()["data"][0])

        # send to google sheet
        worksheet = gc.get_worksheet(0)
        worksheet.append_row(
            list(b_in.model_dump().values())
                )


@app.get("/books")
def get_books(gc: Spreadsheet = Depends(open_worksheet)) -> BooksOut:
    """Get all savwd in gs books
    """
    worksheet = gc.get_worksheet(0)
    books = worksheet.get_all_values()
    return BooksOut(books=[
        BookIn(**{
            k:v
            for k,v
            in zip(BookIn.model_fields.keys(), b)
                }) for b in books
            ])
