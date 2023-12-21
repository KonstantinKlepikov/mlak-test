"""
Напишите генератор, используя регулярное выражение,
для поиска всех email-адресов в текстовом файле Напишите программу,
которая использует, написанный генератор для копирования в другой файл.
"""
import re
import os
import random
from faker import Faker
from typing import Generator


pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
random.seed(0)
Faker.seed(0)
fake = Faker()


def make_file_with_emails(
    path: str = 'src/data/emails_raw.txt'
        ) -> None:
    """Make file with emails

    Args:
        path (str): path to text file
    """
    result = []
    for _ in range(random.randrange(20, 30)):
        result.append(
            fake.text(
                max_nb_chars=random.randrange(10, 20)
                    ).rstrip('.')
                )
        result.append(fake.ascii_email())

    with open(os.path.abspath(path), 'w') as file:
        file.write(' '.join(result))


def get_emails(t: str, pattern: str) -> Generator:
    """Parse and get emails from string

    Args:
        t (str): text for parsing
        pattern (str): search pattern

    Returns:
        str: email
    """
    emails = re.findall(pattern, t)
    for e in emails:
        yield e


def make_file_with_parsed_emails(
    path_to_raw_file: str = 'src/data/emails_raw.txt',
    path_to_parsed_file: str = 'src/data/emails_parsed.txt',
        ) -> None:
    """Parse emails from one file to another

    Args:
        path_to_raw_file (str, optional): path to raw text file.
        path_to_raw_file (str, optional): path to parsed text file.
    """
    with open(os.path.abspath(path_to_raw_file), 'r') as file1:
        with open(os.path.abspath(path_to_parsed_file), 'a') as file2:
            file2.truncate(0)
            for line in get_emails(file1.read(), pattern):
                file2.write(line+'\n')



if __name__ == '__main__':

    make_file_with_emails()
    make_file_with_parsed_emails()
