"""
Создайте базу данных SQLite с таблицей "Сотрудники" (поля: id, имя, зарплата).
Напишите клиент для работы с БД, реализовав CRUD операции.
"""
import sqlite3
from sqlite3 import Connection
from typing import Any


class Employees:
    """Employees db class operations

    Database place in memory. Connection is a singletone pattern.
    """
    sqlite_con: Connection | None = None

    @classmethod
    def get_connection(cls) -> Connection:
        """Get sqlite3 connection session

        Returns:
            Connection | None: connection object. Default to None.
        """
        if cls.sqlite_con is None:
            cls.sqlite_con = sqlite3.connect("file::memory:?cache=shared")

        return cls.sqlite_con

    @classmethod
    def close_connection(cls) -> None:
        """Close sqlite3 connection
        """
        if cls.sqlite_con:
            cls.sqlite_con.close()
            cls.sqlite_con = None

    def init_db(self) -> None:
        """Create tables
        """
        con = self.get_connection()
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS "
            "employees(id integer primary key autoincrement, "
            "name text, salary integer)"
                )
        cur.close()

    def get(self, id: int) -> dict[str, Any] | None:
        """Get employee by id
        """
        con = self.get_connection()
        cur = con.cursor()
        result = cur.execute(
            "SELECT * FROM employees WHERE id = ?",
            (id, )
                )
        res = result.fetchone()
        cur.close()
        return res

    def create(self, name: str, salary: int) -> None:
        """Create new employee
        """
        con = self.get_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO employees (name, salary) VALUES (?, ?)",
            (name, salary)
                )
        cur.close()

    def update(
        self,
        id: int,
        name: str | None = None,
        salary: int | None = None
            ) -> None:
        """_Update employee
        """
        con = self.get_connection()
        cur = con.cursor()
        if name is not None:
            cur.execute(
                "UPDATE employees SET name=? WHERE id=?",
                (name, id)
                    )
        if salary is not None:
            cur.execute(
                "UPDATE employees SET salary=? WHERE id=?",
                (salary, id)
                    )
        cur.close()

    def delete(self, id: int) -> None:
        """Delete employee
        """
        con = self.get_connection()
        cur = con.cursor()
        cur.execute(
            "DELETE FROM employees WHERE id=?",
            (id, )
                )
        cur.close()


if __name__ == '__main__':

    db = Employees()
    db.init_db()

    db.create(name='Donald Trump', salary=10000)
    print(db.get(id=1))

    db.update(id=1, salary=3000)
    print(db.get(id=1))

    db.delete(id=1)
    print(db.get(id=1))

    db.create(name='Obama', salary=0)
    print(db.get(id=2))

    db.close_connection()


"""
А вот так это видит chatgpt

Вот пример кода для создания базы данных SQLite с таблицей "Сотрудники" и клиента на Python для работы с ней, реализующего CRUD операции:

import sqlite3

# Создание базы данных и таблицы
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

#create table
cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT, salary REAL)''')

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

def create_employee(employee):
    # Добавление сотрудника в таблицу
    cursor.execute("INSERT INTO employees (name, salary) VALUES (?, ?)",
                   (employee.name, employee.salary))
    conn.commit()
    print("Сотрудник добавлен успешно!")

def read_all_employees():
    # Получение всех сотрудников из таблицы
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Имя: {row[1]}, Зарплата: {row[2]}")

def read_employee(id):
    # Получение сотрудника по ID из таблицы
    cursor.execute("SELECT * FROM employees WHERE id=?", (id,))
    row = cursor.fetchone()
    if row:
        print(f"ID: {row[0]}, Имя: {row[1]}, Зарплата: {row[2]}")
    else:
        print("Сотрудник не найден!")

def update_employee(id, new_name, new_salary):
    # Обновление сотрудника в таблице
    cursor.execute("UPDATE employees SET name=?, salary=? WHERE id=?",
                   (new_name, new_salary, id))
    conn.commit()
    print("Сотрудник обновлен успешно!")

def delete_employee(id):
    # Удаление сотрудника из таблицы
    cursor.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    print("Сотрудник удален успешно!")

# Пример использования CRUD операций
employee1 = Employee("Иван", 1000)
create_employee(employee1)

employee2 = Employee("Петр", 1500)
create_employee(employee2)

read_all_employees()

read_employee(1)

update_employee(2, "Алексей", 2000)

delete_employee(1)

cursor.close()
conn.close()

Этот пример демонстрирует создание таблицы "Сотрудники", добавление сотрудников, получение всех сотрудников, получение сотрудника по ID, обновление данных сотрудника и удаление сотрудника из таблицы.

Обратите внимание, что код генерирует базу данных 'employees.db' и все операции выполнены через объект conn и cursor базы данных SQLite3.
"""
