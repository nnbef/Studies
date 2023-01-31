import sys
from Parsers import ArgParser, Parse
from Savers import SaveData


if __name__ == '__main__':
    print('Application started with arguments:',
          str(sys.argv[1:]).replace('[', '').
          replace(']', '').replace("'", ''))
    argParser = ArgParser()
    arguments = argParser.parse_args(sys.argv[1:])
    data = Parse(arguments.startDate, arguments.currency)
    SaveData(data, arguments.outputFile, arguments.format)
