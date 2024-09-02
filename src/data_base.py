import os

import psycopg2
from dotenv import load_dotenv

from src.abstract_classes import CreatorDB


class DBCreator(CreatorDB):
    """Класс по работе с базой данных.
    Класс позволяет создавать базу данных с заданным названием,
    а также создавать таблицы в сохданной базе данных.
    Класс является дочерним классом класса CreatorDB."""

    def __init__(self, db_name: str = "test_base") -> None:
        self.db_name = db_name

    def create_db(self) -> None:
        """Метод создаёт базу данных с заданным названием."""
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_database = os.getenv("DB_DATABASE")
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_database, user=db_user, password=db_password)
        cur = conn.cursor()
        conn.autocommit = True
        try:
            sql = f"CREATE DATABASE {self.db_name}"
            cur.execute(sql)
        except Exception:
            raise ValueError("Ошибка при создании базы данных.")
        finally:
            cur.close()
            conn.close()

    def create_table(self) -> None:
        """Метод создаёт таблицы с заданными названиями."""
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        conn = psycopg2.connect(host=db_host, port=db_port, database=self.db_name, user=db_user, password=db_password)
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
