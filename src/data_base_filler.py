import os

import psycopg2
from dotenv import load_dotenv

from src.abstract_classes import DataBase


class DBFiller(DataBase):
    """Класс по работе с базой данных.
    Класс позволяет заполнять данными таблицы базы данных.
    Класс является дочерним классом класса DataBase."""

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    def db_connect(self) -> None:
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        self.conn = psycopg2.connect(
            host=db_host, port=db_port, database=self.db_name, user=db_user, password=db_password
        )

    def fill_the_tablet(self, data: list) -> None:
        """Метод заполняет таблицы базы данных."""
        self.db_connect()
        cur = self.conn.cursor()
        try:
            for item in data:
                # Проверяем наличие записи компании в таблице с компаниями, чтобы избежать дублирования.
                # Получаем id компании и проставляем его в соответствующей графе в таблице вакансий.
                cur.execute(f"SELECT EXISTS (SELECT * FROM companies WHERE company_name = '{item['employer']}')")
                if cur.fetchone()[0]:
                    cur.execute(f"SELECT company_id FROM companies WHERE company_name = '{item['employer']}'")
                    id = cur.fetchone()[0]
                    sql_vacs = """INSERT INTO vacancies
                                  (company_id, vacancy_name, salary, link, description, requirement)
                                  VALUES (%s, %s, %s, %s, %s, %s)"""
                    cur.execute(
                        sql_vacs,
                        (id, item["title"], item["salary"], item["link"], item["description"], item["requirement"]),
                    )
                    self.conn.commit()

                else:
                    cur.execute(f"INSERT INTO companies (company_name) VALUES ('{item['employer']}')")
                    self.conn.commit()
                    cur.execute(f"SELECT company_id FROM companies WHERE company_name = '{item['employer']}'")
                    id = cur.fetchone()[0]
                    sql_vacs = """INSERT INTO vacancies
                                  (company_id, vacancy_name, salary, link, description, requirement)
                                  VALUES (%s, %s, %s, %s, %s, %s)"""
                    cur.execute(
                        sql_vacs,
                        (id, item["title"], item["salary"], item["link"], item["description"], item["requirement"]),
                    )
                    self.conn.commit()

                self.conn.commit()
            print("Таблицы компаний и вакансий успешно заполнены.")

        except Exception:
            raise ValueError("Ошибка при заполнении базы данных.")
        finally:
            cur.close()
            self.conn.close()
