import psycopg2


class DBCreator:
    """Класс по работе с базой данных.
    Класс позволяет создавать базу данных с заданным названием,
    а также создавать таблицы в сохданной базе данных."""

    # def __init__(self, db_name, db_host, db_port, db_user, db_password):
    # self.db_name = db_name
    # self.db_host = db_host
    # self.db_port = db_port
    # self.db_user = db_user
    # self.db_password = db_password

    def __init__(self, db_name):
        self.db_name = db_name

    def create_db(self):
        """Метод создаёт базу данных с заданным названием."""
        conn = psycopg2.connect(host="localhost", port="5432", database="postgres", user="postgres", password="12345")
        cur = conn.cursor()
        conn.autocommit = True
        try:
            sql = f"CREATE DATABASE {self.db_name}"
            cur.execute(sql)
            print("База данных успешно создана")
        except Exception:
            raise ValueError("Ошибка при создании базы данных.")
        finally:
            cur.close()
            conn.close()

    def create_table(self):
        """Метод создаёт таблицы с заданными названиями."""
        conn = psycopg2.connect(
            host="localhost", port="5432", database=self.db_name, user="postgres", password="12345"
        )
        cur = conn.cursor()
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
        cur.close()
        conn.close()


if __name__ == "__main__":
    db = DBCreator("test_base")
    db.create_db()
    db.create_table()
