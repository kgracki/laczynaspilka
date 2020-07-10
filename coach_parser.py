#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : coach_parser.py
# Author            : Kacper Gracki <kacpergracki@gmail.com>
# Date              : 11.05.2020
# Last Modified Date: 11.05.2020
# Last Modified By  : Kacper Gracki <kacpergracki@gmail.com>

import sys
import requests
from bs4 import BeautifulSoup


class CoachParser(object):
    class Coach(object):
        def __init__(self,
                     name: str,
                     lastname: str,
                     state: str,
                     licence_type: str,
                     licence: str,
                     expiration_date: str):
            self.name: str = name
            self.lastname: str = lastname
            self.state: str = state
            self.licence_type: str = licence_type
            self.licence: str = licence
            self.expiration_date: str = expiration_date

        def __repr__(self):
            return f'Name: {self.name}\n'\
                   f'Lastname: {self.lastname}\n'\
                   f'State: {self.state}\n'\
                   f'Licence Type: {self.licence_type}\n'\
                   f'Licence: {self.licence}\n'\
                   f'Expiration Date: {self.expiration_date}\n'

    def __init__(self):
        pass

    def _parse_coach_data(self, name: str, lastname: str) -> []:
        url = f'https://www.laczynaspilka.pl/trenerzy,1.html?type={name}+{lastname}&voivodeship=0&licence=0&submit=Filtruj'
        coach_list = []
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find(class_='table-ranking')
            try:
                table_body = table.find('tbody')
                table_rows = table_body.find_all('tr')
                for row in table_rows:
                    cols = row.find_all('td')
                    table_elements = [element.text.strip() for element in cols]
                    coach_list.append(table_elements)
            except Exception:
                pass

        return coach_list

    def get_coach_info(self, name, lastname):
        table_elements = self._parse_coach_data(name=name, lastname=lastname)
        if table_elements:
            for element in table_elements:
                coach = self._get_coach_instance(element)
                print(coach)
        else:
            print(f'No information found for coach {name} {lastname}')

    def _get_coach_instance(self, elements):
        return CoachParser.Coach(
            lastname=elements[0],
            name=elements[1],
            state=elements[2],
            licence_type=elements[3],
            licence=elements[4],
            expiration_date=elements[5]
        )


if __name__ == '__main__':
    name = str(sys.argv[1])
    lastname = str(sys.argv[2])
    coach_parser = CoachParser()
    coach_parser.get_coach_info(name=name, lastname=lastname)
