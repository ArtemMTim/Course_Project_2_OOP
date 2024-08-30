from abc import ABC, abstractmethod


class CreatorDB(ABC):
    """Абстрактный метод по созданию базы данных и таблиц."""

    @abstractmethod
    def create_db(self):
        pass

    @abstractmethod
    def create_table(self):
        pass


class DataBase(ABC):
    """Абстрактный метод по взаимодействию с базой данных."""

    @abstractmethod
    def db_connect(self):
        pass
