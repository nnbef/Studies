from datetime import date as dtDate


class RowFromTable:
    def __init__(self, date, count, curs):
        date = date.get_text().split('.')
        date.reverse()
        self.__date = dtDate.fromisoformat('-'.join(date))
        self.__count = int(count.get_text())
        self.__curs = float(curs.get_text().replace(',', '.'))

    def GetData(self):
        return [self.__date, self.__count, self.__curs]
