import csv
import os
import re

from activityanalyzer.logger.logger import get_logger


class CsvParser:
    def __init__(self, file_path):
        self._file_path = file_path
        self._space_pattern = re.compile(r' +')

        self._log = get_logger('CsvParser', __name__)

        if not os.path.exists(file_path):
            self._log.error("Csv file path doesn't exist: '{}'".format(file_path))

    def get_row_generator(self, *row_filters):
        """
        Returns a generator for iterating over csv files.
        :param row_filters: row filter functions
        :return: generator of rows passing filter functions
        """
        with open(self._file_path, 'r') as file:
            # Detect row delimiter and quote characters
            dialect = csv.Sniffer().sniff(str(file.readlines(5)), [',', ';'])
            reader = csv.reader(file, dialect)
            file.seek(0)

            for row in reader:
                # Clean rows by deleting multiple white spaces
                row = [re.sub(self._space_pattern, ' ', col).strip() for col in row]
                if self.apply_row_filters(row, *row_filters):
                    yield row

    @staticmethod
    def apply_row_filters(row, *row_filters):
        """
        Applies filter functions on row and connects them logically AND
        :param row: list of elements
        :param row_filters: filter functions
        :return: row passes tests status
        """
        valid_row = True
        for row_filter in row_filters:
            valid_row = valid_row and row_filter(row)
            if not valid_row:
                break
        return valid_row


if __name__ == '__main__':
    file_path1 = '../../data/comdirect_01_2019.csv'
    file_path2 = '../../data/dkb_2018.csv'

    a = CsvParser(file_path2).get_row_generator()
    for line in a:
        print(str(line))
