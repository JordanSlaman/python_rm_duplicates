import csv
import unittest

from remove_duplicates import identify
from remove_duplicates.validate_paths import validate_csv

from .fixtures import TestData


class IdentifyTestCase(unittest.TestCase):

    def setUp(self):
        self.test_data = TestData()
        self.identify_filename = 'test_identify.csv'

    def tearDown(self):
        self.test_data.delete()

    def test_identify(self):

        passed_path_names = self.test_data.args_paths
        identified_csv_filepath = validate_csv(self.test_data.args_found_duplicates_csv_filepath)

        identify(passed_path_names,
                 outfile=identified_csv_filepath,
                 recurse=self.test_data.args_recurse,
                 progress=self.test_data.args_progress)

        with open(self.identify_filename, newline='') as csvfile:
            identity_reader = csv.reader(csvfile)
            for row in identity_reader:
                for file_name in row[1:]:
                    assert 'dupe' in file_namee


if __name__ == '__main__':
    unittest.main()

    # identify_filename = test_dir_name + 'test_idenfify.csv'
