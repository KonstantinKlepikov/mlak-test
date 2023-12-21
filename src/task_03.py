"""
Что получится в результате двух вычислений? Почему?
t = (1, 2, [50, 60])
t[2] += [10, 20]
"""

t = (1, 2, [50, 60])
t[2] += [10, 20]

print(t)

"""TypeError: 'tuple' object does not support item assignment

Проблема в присваивании для tuple - т.к. кортеж иммутабелен,
то он не поддерживает данный протокол.

Между тем, список, входящий в кортеж, мутабельный оюъект.
Мы можем сделать так:

t[2].extend([10, 20])
"""
