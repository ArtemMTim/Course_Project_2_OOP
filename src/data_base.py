import psycopg2

from config import config
from src.abstract_classes import CreatorDB


class DBCreator(CreatorDB):
    """Класс по работе с базой данных.
    Класс позволяет создавать базу данных с заданным названием,
    а также создавать таблицы в сохданной базе данных.
    Класс является дочерним классом класса CreatorDB."""

    def __init__(self, db_name: str = "test_base") -> None:
        self.db_name = db_name
        self.params = config()

    def create_db(self) -> None:
        """Метод создаёт базу данных с заданным названием."""

        conn = psycopg2.connect(database="postgres", **self.params)
        cur = conn.cursor()
        conn.autocommit = True
        try:
            sql = f"DROP DATABASE IF EXISTS {self.db_name}"
            cur.execute(sql)
            sql = f"CREATE DATABASE {self.db_name}"
            cur.execute(sql)
        except Exception:
            raise ValueError("Ошибка при создании базы данных.")
        finally:
            cur.close()
            conn.close()

    def create_table(self) -> None:
        """Метод создаёт таблицы с заданными названиями."""

        conn = psycopg2.connect(database=self.db_name, **self.params)
        cur = conn.cursor()
        try:
            cur.execute(
                """CREATE TABLE if not exists companies
                       (company_id SMALLSERIAL PRIMARY KEY,
                       company_name text NOT NULL);"""
            )

            cur.execute(
                """CREATE TABLE if not exists vacancies
                        (vacancy_id SMALLSERIAL PRIMARY KEY,
                        company_id INT NOT NULL,
                        vacancy_name text NOT NULL,
                        salary INT NOT NULL,
                        link text NOT NULL,
                        description text NOT NULL,
                        requirement text NOT NULL,
                        FOREIGN KEY (company_id)
                        REFERENCES companies(company_id));"""
            )
            conn.commit()
        except Exception:
            raise ValueError("Ошибка при создании таблиц базы данных.")
        finally:
            cur.close()
            conn.close()
