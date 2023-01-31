from RowFromTable import RowFromTable
from datetime import date as dtDate
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import argparse


class URLBuilder:
    def __init__(self, currency, startDate):
        currencyDict = {'usd': '1235', 'eur': '1239'}
        currency = currency if currency.isdigit() else currencyDict[currency.lower()]
        currentDate = datetime.now()
        currentDate = f'{currentDate.day}.{currentDate.month}.{currentDate.year}'
        self.__url = 'https://www.cbr.ru/currency_base/dynamics/'
        self.__url += '?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1'
        self.__url += '&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R0'
        self.__url += currency
        self.__url += '&UniDbQuery.From=' + startDate
        self.__url += '&UniDbQuery.To=' + currentDate

    def GetURL(self):
        return self.__url


def ArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--startDate', default='01.01.2005')
    parser.add_argument('--currency', default='USD')
    parser.add_argument('--outputFile',
                        default=f'ParseFile {datetime.now().day}.{datetime.now().month}.{datetime.now().year}')

    parser.add_argument('--format', default='csv')
    return parser


def Parse(startDate, currency):
    print('Start of parsing')
    try:
        urlBuilder = URLBuilder(currency, startDate)
        page = requests.get(urlBuilder.GetURL())
        bs = BeautifulSoup(page.text, "lxml")
        table = bs.find('table', 'data')
        print('Currency:',
              table.find('td').get_text().replace('\n', ''))
        data = []
        rows = table.find_all('td')
        print('\tStart cleaning table')
        clearRows = []
        for row in rows:
            try:
                date = row.get_text().split('.')
                date.reverse()
                dtDate.fromisoformat('-'.join(date))
                clearRows.append(row)
                continue
            except Exception:
                pass
            try:
                int(row.get_text())
                clearRows.append(row)
                continue
            except Exception:
                pass
            try:
                float(row.get_text().replace(',', '.'))
                clearRows.append(row)
                continue
            except Exception:
                pass
        rows = clearRows
        print('\tCleaning table completed successfully')
        for i in range(-1, -len(rows), -3):
            data.append(RowFromTable(rows[i - 2], rows[i - 1], rows[i]))
    except Exception:
        print("Failed to parse site")
        exit()
    else:
        print('Parsing completed successfully')
        return data
