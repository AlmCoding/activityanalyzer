import unittest

from activityanalyzer.csvparser.shared_row_filters import RowSizeFilter


class TestCsvParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_RowSizeFilter(self):

        test_data = [["11", "12", "13"],
                     ["21", "22"],
                     ["31"],
                     []]

        # Test SHORTER
        response = [RowSizeFilter(RowSizeFilter.Match.SHORTER, size=2).filter(row) for row in test_data]
        # Check correct values
        solution = [bool(i) for i in [0, 0, 1, 1]]
        self.assertEqual(solution, response)

        # Test SHORTER_EQUAL
        response = [RowSizeFilter(RowSizeFilter.Match.SHORTER_EQUAL, size=2).filter(row) for row in test_data]
        # Check correct values
        solution = [bool(i) for i in [0, 1, 1, 1]]
        self.assertEqual(solution, response)

        # Test EQUAL
        response = [RowSizeFilter(RowSizeFilter.Match.EQUAL, size=2).filter(row) for row in test_data]
        # Check correct values
        solution = [bool(i) for i in [0, 1, 0, 0]]
        self.assertEqual(solution, response)

        # Test LONGER_EQUAL
        response = [RowSizeFilter(RowSizeFilter.Match.LONGER_EQUAL, size=2).filter(row) for row in test_data]
        # Check correct values
        solution = [bool(i) for i in [1, 1, 0, 0]]
        self.assertEqual(solution, response)

        # Test LONGER
        response = [RowSizeFilter(RowSizeFilter.Match.LONGER, size=2).filter(row) for row in test_data]
        # Check correct values
        solution = [bool(i) for i in [1, 0, 0, 0]]
        self.assertEqual(solution, response)


if __name__ == '__main__':
    unittest.main()
