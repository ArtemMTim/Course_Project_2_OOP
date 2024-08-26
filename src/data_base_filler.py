import psycopg2


class DBFiller:
    """Класс по работе с базой данных.
    Класс позволяет заполнять данными таблицы базы данных."""

    def __init__(self, db_name):
        self.db_name = db_name

    def fill_the_tablet(self, data):
        """Метод заполняет таблицы базы данных."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()

        try:
            for item in data:
                cur.execute(f"SELECT EXISTS (SELECT * FROM companies WHERE company_name = '{item['employer']}')")
                if cur.fetchone()[0]:
                    cur.execute(f"SELECT company_id FROM companies WHERE company_name = '{item['employer']}'")
                    id = cur.fetchone()[0]
                    sql_vacs = """INSERT INTO vacancies (company_id, vacancy_name, salary, link, description, requirement) VALUES (%s, %s, %s, %s, %s, %s)"""
                    cur.execute(
                        sql_vacs,
                        (id, item["title"], item["salary"], item["link"], item["description"], item["requirement"]),
                    )
                    conn.commit()

                else:
                    cur.execute(f"INSERT INTO companies (company_name) VALUES ('{item['employer']}')")
                    conn.commit()
                    cur.execute(f"SELECT company_id FROM companies WHERE company_name = '{item['employer']}'")
                    id = cur.fetchone()[0]
                    sql_vacs = """INSERT INTO vacancies (company_id, vacancy_name, salary, link, description, requirement) VALUES (%s, %s, %s, %s, %s, %s)"""
                    cur.execute(
                        sql_vacs,
                        (id, item["title"], item["salary"], item["link"], item["description"], item["requirement"]),
                    )
                    conn.commit()

                conn.commit()
            print("Таблицы компаний и вакансий успешно заполнены.")

        except Exception:
            raise ValueError("Ошибка при заполнении базы данных.")
        finally:
            cur.close()
            conn.close()
