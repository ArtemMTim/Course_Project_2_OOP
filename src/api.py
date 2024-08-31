from abc import ABC, abstractmethod
from typing import Any, List

import requests


class Parser(ABC):
    """Абстрактный класс по работе с API сервисами."""

    @abstractmethod
    def load_vacancies(self) -> None:
        pass

    @abstractmethod
    def export_vac_list(self) -> List[Any]:
        pass


class HH(Parser):
    """Класс для работы с API сервиса HeadHunter.
    Получает список вакансий по ключевому слову.
    Полученный список приводит к необходимому виду, описанному в README.
    Класс является дочерним классом класса Parser."""

    def __init__(self) -> None:
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"employer_id": "", "area": 113, "page": 0, "per_page": 100}
        self.vacancies = []
        self.vacancies_for_base = []

    def load_vacancies(self, id: list[Any]) -> None:
        """Метод загружает вакансии с сервиса HH. Формирует из загруженных данных список объектов
        вакансий с полями: название, ссылка, зарплата, описание, требования, место."""
        self.params["employer_id"] = id
        while self.params.get("page") != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            self.params["page"] += 1
        for vacancie in self.vacancies:
            if vacancie["employer"]["name"]:
                employer = vacancie["employer"]["name"]
                if vacancie["name"]:
                    title = vacancie["name"]
                else:
                    title = "Не указано."
                if vacancie["alternate_url"]:
                    link = vacancie["alternate_url"]
                else:
                    link = "Не указано."
                if vacancie["snippet"]["responsibility"]:
                    description = vacancie["snippet"]["responsibility"]
                else:
                    description = "Не указано."
                if vacancie["snippet"]["requirement"]:
                    requirement = vacancie["snippet"]["requirement"]
                else:
                    requirement = "Не указано."

                if vacancie["salary"]:
                    if vacancie["salary"]["from"]:
                        salary = vacancie["salary"]["from"]
                    elif vacancie["salary"]["to"]:
                        salary = vacancie["salary"]["to"]
                    else:
                        salary = 0
                else:
                    salary = 0

                if vacancie["area"]["name"]:
                    area = vacancie["area"]["name"]
                else:
                    area = "Не указано."
                self.vacancies_for_base.append(
                    {
                        "employer": employer,
                        "title": title,
                        "link": link,
                        "description": description,
                        "requirement": requirement,
                        "salary": salary,
                        "area": area,
                    }
                )

    def export_vac_list(self) -> list:
        """Метод возвращает обработанный по заданным критериям список вакансий."""
        return self.vacancies_for_base
