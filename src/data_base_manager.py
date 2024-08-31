import psycopg2

from src.abstract_classes import DataBase


class DBManager(DataBase):
    """Класс по работе с базой данных.
    Класс позволяем получать выборку из базы данных по различным признакам.
    Класс является дочерним классом класса DataBase."""

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    def db_connect(self) -> None:
        self.conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Метод возвращает выборку по вакансиям.
        В выборке присутствуют столбцы: название компании, количество вакансий указанной компании."""
        self.db_connect()
        cur = self.conn.cursor()
        sql = """SELECT company_name, COUNT(*) AS vacancies_count
                 FROM companies
                 JOIN vacancies ON companies.company_id = vacancies.company_id
                 GROUP BY company_name"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        self.conn.close()
        return result

    def get_all_vacancies(self) -> list[tuple]:
        """Метод возвращает выборку по всем вакансиям.
        В выборке присутствуют столбцы: название компании, название вакансии, зарплата, сылка на вакансию."""
        self.db_connect()
        cur = self.conn.cursor()
        sql = """SELECT company_name, vacancy_name, salary, link
                 FROM companies
                 JOIN vacancies ON companies.company_id = vacancies.company_id"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        self.conn.close()
        return result

    def get_avg_salary(self) -> list[tuple]:
        """Метод возвращает среднюю зарплату по вакансиям."""
        self.db_connect()
        cur = self.conn.cursor()
        sql = """SELECT round(AVG(salary), 2) AS avg_salary
                 FROM vacancies"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        self.conn.close()
        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Метод возвращает выборку по вакансиям, у которых зарплата выше средней по вакансиям.
        В выборке присутствуют столбцы: название компании, название вакансии, зарплата, сылка на вакансию."""
        self.db_connect()
        cur = self.conn.cursor()
        sql = """SELECT company_name, vacancy_name, salary, link
                 FROM companies
                 JOIN vacancies ON companies.company_id = vacancies.company_id
                 WHERE salary > (SELECT round(AVG(salary), 2) FROM vacancies)
                 ORDER BY company_name, salary DESC"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        self.conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Метод возвращает выборку по вакансиям, у которых присутствует ключевое слово в названии.
        В выборке присутствуют столбцы: название компании, название вакансии, зарплата, сылка на вакансию."""
        self.db_connect()
        cur = self.conn.cursor()
        sql = f"""SELECT company_name, vacancy_name, salary, link
                  FROM companies
                  JOIN vacancies ON companies.company_id = vacancies.company_id
                  WHERE vacancy_name LIKE '%{keyword}%'"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        self.conn.close()
        return result
