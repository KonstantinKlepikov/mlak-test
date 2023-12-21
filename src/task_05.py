"""
Создайте текстовый файл с несколькими строками текста.
Напишите функцию, которая читает файл и выводит количество слов в каждой строке.
"""
import os


def word_count(path: str = 'src/data/example.txt') -> None:
    """Count a words in rows and print result

    Args:
        path (str): path to text file
    """
    with open(os.path.abspath(path), 'r') as file:
        for row in file:
            print(len(row.split(' ')))


if __name__ == '__main__':

    word_count()
