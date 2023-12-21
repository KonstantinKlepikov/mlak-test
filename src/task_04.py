"""
Напишите функцию, которая принимает строку и возвращает ее перевернутую версию.
Напишите функцию, которая проверяет, является ли строка палиндромом.
"""
import re


def reverse_str(i: str) -> str:
    """Reverse any string

    Args:
        i (str): given string

    Returns:
        str: reversed result
    """
    return i[::-1]


def is_palindrome(i: str) -> bool:
    """Check is a string a palindrom.

    Args:
        i (str): given string

    Returns:
        bool
    """
    j = reverse_str(i)
    return i == j


def is_palindrome_letter(i: str) -> bool:
    """Check is a letters of string a palindrom.

    Args:
        i (str): given string

    Returns:
        bool
    """
    i = re.sub(r'[\W\d_]+', '', i).lower()
    j = reverse_str(i)
    return i == j


if __name__ == '__main__':

    print(reverse_str('This is fine'))
    print(is_palindrome('Аргентина манит негра!'))
    print(is_palindrome_letter('Аргентина манит негра!'))
