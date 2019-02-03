import unittest
import types
import os

from activityanalyzer.csvparser.CsvParser import CsvParser


class TestCsvParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def create_tmp_csv_file(rows):
        """
        Create temporary csv file for unittests.
        :param rows: list of rows
        :return: file path
        """
        path = "tests/tmp.csv"
        n = 1
        while os.path.exists(path):
            path = "tests/tmp{}.csv".format(n)
            n += 1

        with open(path, "w") as file:
            for row in rows:
                if type(row) is str:
                    file.write(row + "\n")
                elif type(row) is list:
                    file.write(";".join(row) + "\n")
        return path

    @staticmethod
    def delete_tmp_csv_file(path):
        """ Delete file """
        if os.path.exists(path):
            os.remove(path)

    def test_get_row_generator(self):

        test_data = [["11", "12", "13"],
                     ["21", "22", "23"],
                     ["31", "32", "33"],
                     ["''", "&", "@"],
                     []]
        # Create test file
        file_path = TestCsvParser.create_tmp_csv_file(test_data)

        generator = CsvParser(file_path).get_row_generator()
        # Check generator typ
        self.assertIsInstance(generator, types.GeneratorType)
        # Check correct values
        self.assertEqual(test_data, [row for row in generator])

        # Delete test file
        TestCsvParser.delete_tmp_csv_file(file_path)

    def test_apply_row_filters(self):
        test_data = [["11", "12", "13"],
                     ["21", "22", "23"],
                     ["31", "32", "33"],
                     ["''", "&", "@"],
                     []]

        # No filters applied
        passed = [row for row in test_data if CsvParser.apply_row_filters(row)]
        self.assertEqual(test_data, passed)


if __name__ == '__main__':
    unittest.main()
