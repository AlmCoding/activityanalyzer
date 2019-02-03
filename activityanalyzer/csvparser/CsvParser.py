import csv
import os


class CsvParser:
    def __init__(self, file_path):
        self._file_path = file_path

        if not os.path.exists(file_path):
            pass

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
    file_path1 = "../../data/comdirect_01_2019.csv"
    file_path2 = "../../dat/dkb_2018.csv"

    #a = CsvFileParser(file_path).get_matrix_head()


    a = CsvParser(file_path1).get_row_generator()
    for line in a:
        print(str(line))








    """
        def get_file_format(self):
            pass

        def transaction_row_filter(self, row):
            if re.match(r'\d\d\.\d\d\.(\d){4}', row[0]):
                return True
            else:
                return False

        def get_matrix_head(self):
            for row in self.get_row_generator(self.transaction_row_filter):
                print(str(row))

        def get_transaction(self, bank):
            return bank.parse(self.get_row_generator)
    """