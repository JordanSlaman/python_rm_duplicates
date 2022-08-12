from pathlib import Path
import tempfile

TEST_DATA = {
    'path1': {
        'first': 'coffee',
        'first_dupe': 'coffee',
        'second': 'bagel',
        'third': 'banana',
        'fourth': 'chocolate'
    },
    'path2': {
        'first_dupe2': 'coffee',
        'first_dupe3': 'coffee',
        'second_dupe': 'bagel',
        'remain': 'tea'
    },
    'path3': {  # all dupes, should be preserved with keep_empty_dirs
        'first_dupe4': 'coffee',
        'first_dupe5': 'coffee',
        'second_dupe2': 'bagel',
        'third_dupe': 'tea'
    }
}


class TestData:

    def __init__(self):

        # Setup Test Data
        print('Setting up test data...')
        self.test_dir = tempfile.TemporaryDirectory()

        # self.test_dir_name = self.test_dir.name + '/'
        self.test_dir_path = Path(self.test_dir.name + '/')
        self.test_dir_top_paths = [self.test_dir_path / test_folder_name for test_folder_name in TEST_DATA.keys()]

        # todo recrsion
        for test_folder_name, data in TEST_DATA.items():
            folder_path = self.test_dir_path / test_folder_name
            folder_path.mkdir(exist_ok=True)

            for file_name, string in data.items():
                file_path = folder_path / f'{file_name}.txt'
                with open(file_path, "w") as file:
                    file.write(f"{string} \n")

        # Setup Args
        self.args_paths = self.test_dir_top_paths
        self.args_dry_run = False
        self.args_found_duplicates_csv_filepath = './duplicates_found.csv'
        self.args_skip_identification = False
        self.args_recurse = False
        self.args_keep_empty_subdirectories = False
        self.args_progress = False
        self.args_verbose = False

    def delete(self):
        print('Cleaning up test data...')
        self.test_dir.cleanup()
