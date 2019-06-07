import re
import enum

from activityanalyzer.csvparser.CsvParser import CsvParser
import activityanalyzer.csvparser.shared_row_filters as srf
from activityanalyzer.Transaction import Transaction


class DkbCsvInterpreter:
    ColumnNames = {
        "booking_date": ("Buchungstag", None),
        "value_date": ("Wertstellung", None),
        "booking_text": ("Buchungstext", None),
        "principal_beneficiary": ("Auftraggeber / Begünstigter", None),
        "reference_line": ("Verwendungszweck", None),
        "account_number": ("Kontonummer", None),
        "amount": ("Betrag (EUR)", None)
    }
    Formats = {
        'decimal_separator': ',',
        'thousands_separator': '.',
        'date_format': '%d.%m.%Y'
    }

    def __init__(self, file_path):

        self._csv_parser = CsvParser(file_path)

        names = get_column_names(self._csv_parser.get_row_generator())
        get_column_indexes(names)

        gen = get_transaction_generator(self._csv_parser.get_row_generator)
        for i in gen:
            pass

        categories = []
        for row in self._csv_parser.get_row_generator(transaction_filter):
            print(row)
            if row[2] not in categories:
                categories.append(row[2])

        for e in categories:
            print(e)


def get_column_names(row_generator):
    new_row = None
    for row in row_generator:
        old_row, new_row = new_row, row
        if transaction_filter(new_row) and len(old_row) == len(new_row):
            while not old_row[-1]:
                old_row.pop()
            return old_row


def get_column_indexes(column_names):
    for key in DkbCsvInterpreter.ColumnNames.keys():
        (name, idx) = DkbCsvInterpreter.ColumnNames[key]
        idx = column_names.index(name)
        DkbCsvInterpreter.ColumnNames[key] = (name, idx)


def get_transaction_generator(get_row_generator):
    for row in get_row_generator(transaction_filter):
        yield Transaction(booking_date=row[DkbCsvInterpreter.ColumnNames['booking_date'][1]],
                          value_date=row[DkbCsvInterpreter.ColumnNames['value_date'][1]],
                          booking_text=row[DkbCsvInterpreter.ColumnNames['booking_text'][1]],
                          principal_beneficiary=row[DkbCsvInterpreter.ColumnNames['principal_beneficiary'][1]],
                          reference_line=row[DkbCsvInterpreter.ColumnNames['reference_line'][1]],
                          account_number=row[DkbCsvInterpreter.ColumnNames['account_number'][1]],
                          amount=row[DkbCsvInterpreter.ColumnNames['amount'][1]],)


def account_filter(row):
    if row:
        return bool(re.match(r'^(Kontonummer:)$', row[0]))
    return False


def period_filter(row):
    if row:
        return bool(re.match(r'^((Von:)|(Bis:))$', row[0]))
    return False


def transaction_filter(row):
    if row:
        return bool(re.match(r'^(\d\d\.\d\d\.\d\d\d\d)$', row[0]))
    return False


if __name__ == '__main__':
    file_path1 = "../../data/comdirect_01_2019.csv"
    file_path2 = "../../data/dkb_2018.csv"

    a = DkbCsvInterpreter(file_path2)

