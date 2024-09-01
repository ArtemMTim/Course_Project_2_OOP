from src.api import HH
from src.data_base import DBCreator
from src.data_base_filler import DBFiller
from user_settings import employers_list
from src.data_base_manager import DBManager


def main_func():
    print('''Вас приветствует программа по работе с вакансиями в базе данных!
    Программа получает вакансии выбранных работодателей с сервиса HH.
    Список работодателей Вы можете изменить в файле user_settings.
    Программа заносит полученные вакансии в базу данных.
    Также программа позволяет делать выборки из базы данных.''')

    db_name = input('Введите название базы данных сюда: ')

    db = DBCreator(db_name)
    db.create_db()
    print('База данных успешно создана.')
    db.create_table()
    print('Таблицы успешно созданы.')

    vacs_list = []
    vacs = HH()

    id_list = [int(item[0]) for item in employers_list]

    vacs.load_vacancies(id_list)
    temp_vacs_list = vacs.export_vac_list()
    vacs_list.extend(temp_vacs_list)

    print('Список вакансий выбранных компаний создан.')

    db_filler = DBFiller(db_name)
    db_filler.fill_the_tablet(vacs_list)
    print('База данных успешно заполнена.')

    print('''Программа позволяет сделать следующие выборки:
    1 - Всех вакансий;
    2 - Компаний и количества их вакансий;
    3 - Средней зарплаты по всем вакансиям;
    4 - Вакансий с зарплатой выше средней;
    5 - Вакансий с ключевым слово в названии.''')
    db_manager = DBManager(db_name)
    db_manager_dict = {'1': db_manager.get_all_vacancies(),
                       '2': db_manager.get_companies_and_vacancies_count(),
                       '3': db_manager.get_avg_salary(),
                       '4': db_manager.get_vacancies_with_higher_salary()}
    user_choice = input('Введите номер желаемой выборки здесь: ')
    if user_choice == '5':
        user_keyword = input('''Вы выбрали выборку вакансий по ключевому слову.
        Введите ключевое слово сюда: ''')
        result_temp = db_manager.get_vacancies_with_keyword(user_keyword)
    else:
        result_temp = db_manager_dict[user_choice]
    result = []
    for item in result_temp:
        result.append(tuple([str(c) for c in item]))
    for item in result:
        print(' <-> '.join(item))


if __name__ == '__main__':
    main_func()
