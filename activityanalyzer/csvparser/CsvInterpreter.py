# -*- coding: iso-8859-1 -*-

import re
import yaml

from activityanalyzer.logger.logger import get_logger
from activityanalyzer.csvparser.CsvParser import CsvParser
from activityanalyzer.Transaction import Transaction


class CsvInterpreter:
    def __init__(self, csv_file_path, yaml_file_path):
        self._csv_file_path = csv_file_path
        self._yaml_file_path = yaml_file_path

        self._log = get_logger('CsvInterpreter', __name__)
        self._csv_parser = CsvParser(csv_file_path)

        self._column_names, self._format_context = self.parse_yaml_file()
        self.check_column_names()

    def parse_yaml_file(self):
        with open(self._yaml_file_path, 'r', encoding='utf-8') as file:
            try:
                data = yaml.load(file)
                return [data['ColumnNames'], data['FormatContext']]
            except yaml.YAMLError as exc:
                print(exc)

    def get_transaction_generator(self):
        for row in self._csv_parser.get_row_generator(self.transaction_filter):
            yield Transaction(row, self._column_names, self._format_context)

    def get_column_names(self):
        new_row = None
        for row in self._csv_parser.get_row_generator():
            old_row, new_row = new_row, row
            if self.transaction_filter(new_row) and len(old_row) == len(new_row):
                while not old_row[-1]:
                    old_row.pop()
                return old_row

    def check_column_names(self):
        column_names = self.get_column_names()
        for key, value in self._column_names.items():
            if value not in column_names:
                self._log.error("Unable to find '{}' column name in csv file. Check yaml config file.".format(value))
            else:
                self._column_names[key] = column_names.index(value)

    @staticmethod
    def transaction_filter(row):
        if row:
            return bool(re.match(r'^(\d\d\.\d\d\.\d\d\d\d)$', row[0]))
        return False


if __name__ == '__main__':
    csv_file = '../../data/dkb_2018.csv'
    yaml_file = 'DeutscheKreditbank.yaml'

    interpreter = CsvInterpreter(csv_file, yaml_file)
    print(interpreter.parse_yaml_file())