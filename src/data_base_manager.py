import psycopg2


class DBManager:
    """Класс по работе с базой данных.
    Класс позволяем получать выборку из базы данных по различным признакам."""

    def __init__(self, db_name):
        self.db_name = db_name

    def get_companies_and_vacancies_count(self):
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
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        sql = """SELECT *
                FROM vacancies
                ORDER BY salary DESC
                LIMIT 5"""
        result = cur.execute(sql)
        cur.close()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        sql = f"""SELECT *
        FROM vacancies
        WHERE vacancy_name LIKE '%{keyword}%' or '{keyword}%' or '%{keyword}'"""
        result = cur.execute(sql)
        cur.close()
        conn.close()
        return result
