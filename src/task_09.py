"""
Разработайте систему для управления банковскими счетами.
Система должна поддерживать следующие возможности:

    1. Создание клиентов и счетов:
        - Клиент может создать учетную запись в банке.
        - У клиента может быть несколько счетов (например, текущий счет, сберегательный счет).

    2. Операции по счету:
        - Клиент может внести деньги на счет.
        - Клиент может снять деньги со счета.
        - Клиент может запросить баланс своего счета.

    3. Транзакции:
        - Вести учет транзакций (операций по счету) с деталями (сумма, дата, тип операции).
        - Интересы по сберегательному счету:
        - Реализовать функциональность начисления процентов по сберегательному счету.

    4. Кредитные счета:
        - Поддержка кредитных счетов с установленным лимитом и ставкой.

    5. История транзакций:
        - Клиент может просмотреть историю транзакций по своему счету.

    6. Защита данных:
        - Обеспечить безопасность данных клиентов, используя принципы инкапсуляции.

    7.  Обработка ошибок:
        -Реализовать обработку ошибок для случаев, например, попытки снятия суммы больше, чем есть на счету.

Эта задача требует создания классов для клиентов, счетов и транзакций,
а также использование принципов наследования, инкапсуляции и полиморфизма.
"""

class Client:
    """Bank client
    """


class Account:
    """Bank account
    """


class Transaction:
    """Bank transaction
    """

if __name__ == '__main__':

    pass