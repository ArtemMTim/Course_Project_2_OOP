import psycopg2


class DBManager:
    """Класс по работе с базой данных.
    Класс позволяем получать выборку из базы данных по различным признакам."""

    def __init__(self, db_name):
        self.db_name = db_name

    def get_companies_and_vacancies_count(self):
        """Метод возвращает выборку по вакансиям.
        В выборке присутствуют столбцы: название компании, количество вакансий указанной компании."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        sql = """SELECT company_name, COUNT(*) AS vacancies_count
                 FROM companies
                 JOIN vacancies ON companies.company_id = vacancies.company_id
                 GROUP BY company_name"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_all_vacancies(self):
        """Метод возвращает выборку по всем вакансиям.
        В выборке присутствуют столбцы: название компании, название вакансии, зарплата, сылка на вакансию."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        sql = """SELECT company_name, vacancy_name, salary, link
                 FROM companies
                 JOIN vacancies ON companies.company_id = vacancies.company_id"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_avg_salary(self):
        """Метод возвращает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        sql = """SELECT round(AVG(salary), 2) AS avg_salary
                 FROM vacancies"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """Метод возвращает выборку по вакансиям, у которых зарплата выше средней по вакансиям.
        В выборке присутствуют столбцы: название компании, название вакансии, зарплата, сылка на вакансию."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        sql = """SELECT company_name, vacancy_name, salary, link
                 FROM companies
                 JOIN vacancies ON companies.company_id = vacancies.company_id
                 WHERE salary > (SELECT round(AVG(salary), 2) FROM vacancies)
                 ORDER BY company_name"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Метод возвращает выборку по вакансиям, у которых присутствует ключевое слово в названии.
        В выборке присутствуют столбцы: название компании, название вакансии, зарплата, сылка на вакансию."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        sql = f"""SELECT company_name, vacancy_name, salary, link
                  FROM companies
                  JOIN vacancies ON companies.company_id = vacancies.company_id
                  WHERE vacancy_name LIKE '%{keyword}%'"""
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
