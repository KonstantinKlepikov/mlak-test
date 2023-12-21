"""
    Какой будет результат выполнения следующего кода? Почему?
b = 10
def f(a):
    print(a)
    print(b)
    b = 15

f(3)

"""

b = 10
def f(a):
    print(a)
    print(b)
    b = 15

f(3)

"""
>>> UnboundLocalError: local variable 'b' referenced before assignment

В innermost области видимости локальная переменная определена позже.
Т.к. она определена, переменная из более объемлющей области затенена.

К примеру так будет работать, т.к. нет объявления внутри:

b = 10
def f(a):
    print(a)
    print(b)
    # b = 15

f(3)

Подробнее тут:
https://docs.python.org/3/tutorial/classes.html#a-word-about-names-and-objects


Чтобы увидеть переменную снаружи можно сделать так:

b = 10
def f(a):
    global b
    print(a)
    print(b)
    b = 15
    print(b)

f(3)
"""
