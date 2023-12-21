"""
Наполните текстовый файл рандомными значениями (побольше),
можете использовать сторонние библиотеки (faker). Напишите декоратор
timeit который принимает значение N для измерения времени работы функции
и примените к прошлому заданию. Если время превышает заданное
N выводить дополнительное уведомление.
"""
from time import time
from task_06 import make_file_with_parsed_emails


def timeit(function, limit=None):
    def wrapper(*args, **kwargs):
        ts = time()
        result = function(*args, **kwargs)
        te = time()
        res = (te-ts) * 1000000
        print(f'Timeit: {res} mks')
        if limit and res > limit:
            print(f'Is to much: {limit=}')
        return result
    return wrapper


if __name__ == '__main__':

    timeit(make_file_with_parsed_emails, 200)()
