import requests
import re
from bs4 import BeautifulSoup


class CorreiosStatus:

    def __init__(self, code, status=' ', date=' '):
        self.__atual_status = status
        self.__atual_date = date
        self.__code = code
        self.__link = 'http://websro.com.br/rastreamento-correios.php?P_COD_UNI={0}'.format(self.__code)

    def check_code(self):

        if not len(self.__code) == 13:
            return False

        return True

    def had_change(self):
        page = requests.get(self.__link)
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.findChildren('table')[0]
        rows = table.findChildren('td')

        status = re.sub('\s+', ' ', rows[1].getText())

        date = rows[0].getText().replace("<br>", "\n")
        date = date.split('\n')[0][:10]

        if self.__atual_status == ' ' and self.__atual_date == ' ':
            self.__atual_status = status
            self.__atual_date = date
            return False

        if not status == self.__atual_status:
            self.__atual_status = status
            self.__atual_date = date
            return True

    def atual_status(self):
        return self.__atual_status

    def atual_date(self):
        return self.__atual_date

    def link(self):
        return self.__link


if __name__ == '__main__':

    s = CorreiosStatus('LS816758501CH')
    s.had_change()
