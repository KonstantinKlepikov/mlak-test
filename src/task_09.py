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
from dataclasses import dataclass, field
from typing import NewType
from decimal import Decimal
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum
import calendar


Id = NewType('Id', int)


class AccountType(Enum):
    CREDIT = 1
    SAVING = 2


@dataclass(frozen=True)
class Transaction(ABC):
    """Account transaction base class
    """
    val: Decimal
    dt: datetime = datetime.utcnow()


@dataclass(frozen=True)
class InTransaction(Transaction):
    """Account income
    """


@dataclass(frozen=True)
class OutTransaction(Transaction):
    """Account outcome
    """


@dataclass
class Account(ABC):
    """Client account abstract class
    """
    account_id: Id
    rate: Decimal
    type: AccountType
    volume: Decimal = Decimal(0)
    dt: datetime = datetime.utcnow()
    transactions: list[Transaction] = field(default_factory=list)

    @abstractmethod
    def check_limit(self, val: Decimal) -> bool:
        """Check is limit not overwelmed

        Args:
            val (Decimal): value to check limit
        """

@dataclass
class SavingAccount(Account):
    """Client saving account
    """
    type: AccountType = AccountType.SAVING

    def check_limit(self, val: Decimal) -> None:
        """Check is limit exceeded

        Args:
            val (Decimal): value to check limit
        """
        if self.volume < val:
            raise ValueError('Money limit exceeded.')

    def add_day_procent(self) -> Decimal:
        """Add procents to volume
        """
        days = 365 if calendar.isleap(datetime.utcnow().year) else 365
        bonus = self.volume * self.rate / Decimal(days)
        self.volume += bonus
        return bonus


@dataclass
class CreditAccount(Account):
    """Client credit account
    """
    limit: Decimal = Decimal(0)
    type: AccountType = AccountType.CREDIT

    def check_limit(self, val: Decimal) -> None:
        """Check is limit exceeded

        Args:
            val (Decimal): value to check limit
        """
        if self.volume + self.limit < val:
            raise ValueError('Money limit exceeded.')


@dataclass
class Client:
    """Bank client
    """
    client_id: Id
    dt: datetime = datetime.utcnow()
    accounts: dict[Id, Account] = field(default_factory=dict)

    @property
    def _account_ids(self) -> list[Id]:
        """Get account idis

        Returns: list[Id]
        """
        return [ac.account_id for ac in self.accounts.values()]

    @staticmethod
    def _make_account(ac_type: AccountType) -> Account:
        """make account class

        Args:
            ac_type (ac_type): type of account
        """
        match ac_type:
            case AccountType.CREDIT:
                ac = CreditAccount
            case AccountType.SAVING:
                ac = SavingAccount
            case _:
                raise ValueError('Wrong account type.')
        return ac

    def _make_account_id(self) -> Id:
        """Make account id

        Returns:
            Id: new account id
        """
        if ids := self._account_ids:
            return Id(max(ids)+1)
        else:
            return Id(1)

    def _is_valid_account_id(self, account_id: Id) -> None:
        """Has client account

        Args:
            account_id (Id): account id

        Raises:
            ValueError: not finded
        """
        if account_id not in self._account_ids:
            raise ValueError('Invalid account id')

    def create_account(
        self, ac_type: AccountType,
        rate: Decimal = Decimal(0)
            ) -> Id:
        """Create new account with given type

        Args:
            ac_type (AccountType): type of account
            rate (Decimal): rate of loan or reward, defaylt to 0

        Returns: Id
        """
        if rate < Decimal(0):
            raise ValueError('Rate must be positive number.')

        ac = self._make_account(ac_type)
        ac_id = self._make_account_id()
        self.accounts[ac_id] = ac(account_id=ac_id, rate=rate)
        return ac_id

    def set_limit(self, account_id: Id, limit: Decimal) -> None:
        """Set limit of credit account

        Args:
            account_id (Id): account id
            limit (Decimal): limit
        """
        if limit < Decimal(0):
            raise ValueError('Limit must be positive number.')

        self._is_valid_account_id(account_id)

        if self.accounts[account_id].type == AccountType.CREDIT:
            self.accounts[account_id].limit = limit

    def add_money(self, account_id: Id, val: Decimal) -> None:
        """Add money to account

        Args:
            account_id (Id): account id
            val (Decimal): amonth of money
        """
        self._is_valid_account_id(account_id)
        if val < Decimal(0):
            raise ValueError('Value must be a positive number.')
        dt = datetime.utcnow()
        self.accounts[account_id].volume += val
        self.accounts[account_id].transactions.append(InTransaction(val, dt))

    def get_money(self, account_id: Id, val: Decimal) -> None:
        """Get money from account

        Args:
            account_id (Id): account id
            val (Decimal): amonth of money
        """
        self._is_valid_account_id(account_id)
        if val < Decimal(0):
            raise ValueError('Value must be a positive number.')
        self.accounts[account_id].check_limit(val)
        dt = datetime.utcnow()
        self.accounts[account_id].volume -= val
        self.accounts[account_id].transactions.append(OutTransaction(val, dt))

    def get_balance(self, account_id: Id) -> Decimal:
        """Get balance for given account id

        Args:
            account_id (Id): account id
        """
        self._is_valid_account_id(account_id)
        return self.accounts[account_id].volume

    def get_transactions(
        self,
        account_id: Id,
        start: datetime | None = None,
        end: datetime | None = None,
            ) -> list[Transaction]:
        """Get history of transactions

        Args:
            account_id (Id): account id
            start (datetime | None, optional): start range. Defaults to None.
            end (datetime | None, optional): end range. Defaults to None.

        Returns:
            list[Transaction]: transactions from range
        """
        self._is_valid_account_id(account_id)
        if start is None:
            start = self.accounts[account_id].dt
        if end is None:
            end = datetime.utcnow()
        return [
            t for t
            in self.accounts[account_id].transactions
            if (start <= t.dt) and (t.dt < end)
                ]

    def add_day_procent(self, account_id: Id) -> None:
        """Add day procent to saving account

        Args:
            account_id (Id): account id
        """
        self._is_valid_account_id(account_id)
        if self.accounts[account_id].type == AccountType.SAVING:
            dt = datetime.utcnow()
            val = self.accounts[account_id].add_day_procent()
            self.accounts[account_id].transactions.append(InTransaction(val, dt))


if __name__ == '__main__':

    from pprint import pprint

    client = Client(client_id=Id(1))

    ac_id = client.create_account(ac_type=AccountType.SAVING, rate=Decimal(12.5))
    client.add_money(ac_id, Decimal(15000))
    client.get_money(ac_id, Decimal(7000))
    client.add_day_procent(ac_id)
    print(client.get_transactions(ac_id))
    print(client.get_balance(ac_id))
    print(''*20)

    ac_id = client.create_account(ac_type=AccountType.CREDIT, rate=Decimal(6.5))
    client.set_limit(ac_id, Decimal(5000))
    try:
        client.get_money(ac_id, Decimal(7000))
    except ValueError as e:
        print(str(e))
    print(client.get_balance(ac_id))
    print(client.get_transactions(ac_id))
    print(''*20)

    pprint(client)


"""
Вот так это увидел ChatGPT.

Ниже представлен пример реализации системы для управления банковскими счетами на языке Python:

from abc import ABC, abstractmethod
from datetime import datetime

class Account(ABC):
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance
        self.transactions = []

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def get_balance(self):
        return self.balance

    def add_transaction(self, amount, transaction_type):
        transaction = {
            'amount': amount,
            'date': datetime.now(),
            'type': transaction_type
        }
        self.transactions.append(transaction)

class CurrentAccount(Account):
    def __init__(self, account_number, balance):
        super().__init__(account_number, balance)

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction(amount, 'deposit')

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Insufficient balance')
        self.balance -= amount
        self.add_transaction(amount, 'withdraw')

class SavingsAccount(Account):
    def __init__(self, account_number, balance, interest_rate):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction(amount, 'deposit')

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Insufficient balance')
        self.balance -= amount
        self.add_transaction(amount, 'withdraw')

    def compute_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.add_transaction(interest, 'interest')

class Customer:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def create_account(self, account_type, account_number, initial_balance, interest_rate=None):
        if account_type == 'current':
            account = CurrentAccount(account_number, initial_balance)
        elif account_type == 'savings':
            if interest_rate is None:
                raise ValueError('Interest rate must be specified for savings account')
            account = SavingsAccount(account_number, initial_balance, interest_rate)
        else:
            raise ValueError('Invalid account type')
        self.accounts.append(account)

    def get_account_balance(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account.get_balance()
        raise ValueError('Account not found')

    def deposit(self, account_number, amount):
        for account in self.accounts:
            if account.account_number == account_number:
                account.deposit(amount)
                return
        raise ValueError('Account not found')

    def withdraw(self, account_number, amount):
        for account in self.accounts:
            if account.account_number == account_number:
                account.withdraw(amount)
                return
        raise ValueError('Account not found')

    def get_transactions(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account.transactions
        raise ValueError('Account not found')

Теперь мы можем создать клиента, добавить счета и выполнять различные операции с этими счетами. Например:

# Создание клиента
customer = Customer('John Doe')

# Создание счетов
customer.create_account('current', '1234567890', 1000)
customer.create_account('savings', '9876543210', 5000, 0.05)

# Внесение депозита
customer.deposit('1234567890', 500)

# Снятие денег
customer.withdraw('9876543210', 1000)

# Получение баланса счета
balance = customer.get_account_balance('1234567890')

# Получение истории транзакций
transactions = customer.get_transactions('9876543210')

Это основной каркас системы для управления банковскими счетами, который можно дополнить или расширить по мере необходимости. Он обеспечивает создание клиентов, учетные записи и транзакции, а также поддерживает операции по счету, начисление процентов по сберегательному счету и обработку ошибок.

"""
