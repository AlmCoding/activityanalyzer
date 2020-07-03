import os
import re
import csv
import enum

from activityanalyzer.logger import get_logger


class CsvParser:
    class FilterLogic(enum.Enum):
        AND = 1
        OR = 2

    def __init__(self, file_paths: iter, encoding='utf-8'):
        self._file_paths = []
        self._encoding = encoding
        self._space_pattern = re.compile(r' +')
        self._log = get_logger('CsvParser.log', __name__)

        for path in file_paths:
            if not os.path.exists(path) or not re.search(r'\.csv$', path):
                self._log.error("File path doesn't exist or invalid file format detected: '{}'".format(path))
            else:
                self._file_paths.append(path)

    def get_row_generator(self, *row_filters) -> iter:
        """
        Returns a generator for iterating over csv files.
        :param row_filters: row filter functions with potential FilterLogic obj
        :return: generator of rows passing filter functions
        """
        if row_filters and not isinstance(row_filters[-1], CsvParser.FilterLogic):
            row_filters = list(row_filters).append(CsvParser.FilterLogic.AND)

        for path in self._file_paths:
            with open(path, 'r', encoding=self._encoding) as file:
                # Detect row delimiter and quote characters
                dialect = csv.Sniffer().sniff(str(file.readlines(5)), [',', ';'])
                reader = csv.reader(file, dialect)
                file.seek(0)
                for row in reader:
                    # Clean rows by deleting multiple white spaces
                    row = tuple(re.sub(self._space_pattern, ' ', col).strip() for col in row)
                    if not row_filters or self.apply_row_filters(row, *row_filters):
                        yield row

    @staticmethod
    def apply_row_filters(row: tuple, *row_filters) -> bool:
        if row_filters[-1] == CsvParser.FilterLogic.AND:
            return CsvParser.apply_row_filters_and(row, *row_filters[:-1])
        else:
            return CsvParser.apply_row_filters_or(row, *row_filters[:-1])

    @staticmethod
    def apply_row_filters_and(row: tuple, *row_filters: iter) -> bool:
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

    @staticmethod
    def apply_row_filters_or(row: tuple, *row_filters: iter) -> bool:
        """
        Applies filter functions on row and connects them logically OR
        :param row: list of elements
        :param row_filters: filter functions
        :return: row passes tests status
        """
        for row_filter in row_filters:
            if row_filter(row):
                return True
        return False


if __name__ == '__main__':
    file_path1 = '../data/comdirect_01_2019.csv'
    file_path2 = '../data/dkb_2018.csv'

    a = CsvParser(file_path2, "iso-8859-1").get_row_generator()
    for line in a:
        print(str(line))
