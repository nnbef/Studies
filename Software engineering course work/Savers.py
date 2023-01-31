import yaml
import json
import xlsxwriter
import csv


class Writer:
    def __init__(self, param):
        print(f'Initialization of {param} writer')

    def WriteData(self, outputFile):
        print(f'Write data to {outputFile} file')


class YamlWriter(Writer):
    def __init__(self, data):
        super().__init__('yaml')
        self.__data = data

    def WriteData(self, outputFile):
        super().WriteData(outputFile + '.yaml')
        data = []
        for line in self.__data:
            data.append(line.GetData())
        with open(outputFile + '.yaml', 'w') as file:
            yaml.dump(data, file)


class TxtWriter(Writer):
    def __init__(self, data):
        super().__init__('txt')
        self.__data = data

    def WriteData(self, outputFile):
        super().WriteData(outputFile + '.txt')
        with open(outputFile + '.txt', 'w') as file:
            for line in self.__data:
                file.write('[' + ', '.join(map(str, line.GetData()) + ']\n'))


class JsonWriter(Writer):
    def __init__(self, data):
        super().__init__('json')
        self.__data = data

    def WriteData(self, outputFile):
        super().WriteData(outputFile + '.json')
        data = []
        for i in range(len(self.__data)):
            x = self.__data[i].GetData()
            date = x[0].isoformat().split('-')
            date.reverse()
            x[0] = '.'.join(date)
            data.append(json.dumps({i: x}))
        data = ', '.join(data)
        with open(outputFile + '.json', 'w') as file:
            file.write(data)


class XlsxWriter(Writer):
    def __init__(self, data):
        super().__init__('xlsx')
        self.__data = data

    def WriteData(self, outputFile):
        super().WriteData(outputFile + '.xlsx')
        data = []
        for i in range(len(self.__data)):
            x = self.__data[i].GetData()
            date = x[0].isoformat().split('-')
            date.reverse()
            x[0] = '.'.join(date)
            data.append(x)
        workbook = xlsxwriter.Workbook(outputFile + '.xlsx')
        worksheet = workbook.add_worksheet()
        for i in range(len(self.__data)):
            worksheet.write_row(i, 0, data[i])
        workbook.close()


class CsvWriter(Writer):
    def __init__(self, data):
        super().__init__('csv')
        self.__data = data

    def WriteData(self, outputFile):
        super().WriteData(outputFile + '.csv')
        data = []
        for i in range(len(self.__data)):
            x = self.__data[i].GetData()
            date = x[0].isoformat().split('-')
            date.reverse()
            x[0] = '.'.join(date)
            data.append(x)
        with open(outputFile + '.csv', 'w') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(data)


def SaveData(data, outputFile, formatFile):
    try:
        if formatFile.lower() == 'yaml':
            writer = YamlWriter(data)
        elif formatFile.lower() == 'txt':
            writer = TxtWriter(data)
        elif formatFile.lower() == 'json':
            writer = JsonWriter(data)
        elif formatFile.lower() == 'xlsx':
            writer = XlsxWriter(data)
        elif formatFile.lower() == 'csv':
            writer = CsvWriter(data)
        else:
            print('Incorrect file format')
            exit()
        writer.WriteData(outputFile)
    except Exception:
        print('Failed to save file')
        exit()
    else:
        print('File saved successfully')
