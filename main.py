from src.api import HH
from src.data_base import DBCreator
from src.data_base_filler import DBFiller
from user_settings import employers_list
from src.data_base_manager import DBManager


def main_func():
    db_name = "test_base"

    db = DBCreator(db_name)
    db.create_db()
    print('База данных создана')
    db.create_table()
    print('Таблицы созданы')

    vacs_list = []

    vacs = HH()

    id_list = [int(item[0]) for item in employers_list]

    vacs.load_vacancies(id_list)
    temp_vacs_list = vacs.export_vac_list()
    vacs_list.extend(temp_vacs_list)

    print('Список вакансий создан')

    db_filler = DBFiller(db_name)
    db_filler.fill_the_tablet(vacs_list)
    print('База данных заполнена')

    db_manager = DBManager(db_name)
    print(db_manager.get_all_vacancies())
    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())
    print(db_manager.get_vacancies_with_keyword('тестир'))


if __name__ == '__main__':
    main_func()
