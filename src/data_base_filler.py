import psycopg2


class DBFiller:
    """Класс по работе с базой данных.
    Класс позволяет заполнять данными таблицы базы данных."""

    def __init__(self, db_name):
        self.db_name = db_name

    def fill_the_vacs_tablet(self, data_vacs, data_comps):
        """Метод заполняет таблицы базы данных."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
        for item in data_vacs:
            sql = """INSERT INTO vacancies (company_id, company_name, 
                vacancy_name, salary, link, description, requirement) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) returning*"""
            cur.execute(sql, item)
        conn.commit()
        for item in data_comps:
            sql = "INSERT INTO companies (company_name) VALUES (%s) returning*"
            cur.execute(sql, item)
        conn.commit()
        cur.close()
        conn.close()
