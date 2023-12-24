# Mlak-test

## Tasks

[link](https://docs.google.com/document/d/1CDqS-_hsJx8Nkbok_2_l0kk20_dWHbm9PqSumM4JZ1E/edit)

Все задачи представлены в виде отдельных файлов в папке `src` и запускаются из корня проекта, кроме 12-ой - она содержится в отдельной папке и запускается из нее. Комментарии к каждой задаче содержатся в файле задачи, кроме 12-й - как запускать стек для 12-й задачи читай ниже.

## Как запускать

- clone repo
- add local python3.10 by virtualenv and activate it (f.e. `virtualenv -p python 3.10 venv`).
- `pip install requirements.txt` to install dependencies

## Task 12

Задача с djangp размещена в папке `src/task_12`, для запуска стека необходимо перейтим в нее

Потребуется добавить `.env` file с таким содержимым

```sh
# postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mybrilliantpassword
POSTGRES_DB=mlak
POSTGRES_SERVER=mlak-postgres
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}:5432/${POSTGRES_DB}

# redis broker url
CELERY_BROKER_URL=redis://mlak-redis:6379/0
```

Для старта проекта необходим docker compose не ниже 3.8 и утилита make.

### Запуск и остановка стека

- `make serve` to run dev mode
- `make down` to stop

Для работы при первом запуске необходимо зайти в контейнер `mlak api`, мигрировать бд и создать суперюзера.

- `python manage.py migrate`
- `python manage.py createsuperuser`

### Для исследования проекта джоступны такие ресурсы

- [app](http://localhost:8201/mlak)
- [admin](http://localhost:8201/admin/)
- [flower](http://localhost:5756/)

### Что сделано

- сделан шедалер на celery
- данные запрашиваются ву стороннего апи (такой же как и в задаче 10) и закгружаются в бд с регулярностью в 10 секун
- страничким рендерятся минимально
- фильтр я сдеть не успел - и так на все задачи 100500 времени ушло
- тестовое щзадание можно сократить в 10 раз. Простите, но это не тестове, а диплом по программированию на python.
