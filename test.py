import csv
from pathlib import Path
import os

from rm_duplicates import identify, remove

base_pathname = os.path.realpath(__file__).rstrip('.py') + '/'
identify_pathname = base_pathname + 'test_idenfify.csv'

test_data = {
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
    }
}

test_paths = [Path(base_pathname + test_folder_name) for test_folder_name in test_data.keys()]


def setup_test():
    print('Setting up test data...')

    base_path = Path(base_pathname)
    base_path.mkdir(exist_ok=True)

    for test_folder_name, data in test_data.items():
        folder_path = base_path / test_folder_name
        folder_path.mkdir(exist_ok=True)

        for file_name, string in data.items():
            file_path = folder_path / f'{file_name}.txt'
            with open(file_path, "w") as file:
                file.write(f"{string} \n")


def verify_identify():
    with open(identify_pathname, newline='') as csvfile:
        identity_reader = csv.reader(csvfile)
        for row in identity_reader:
            for file_name in row[1:]:
                assert 'dupe' in file_name

    print('Identify test passed!')


def verify_remove():
    for test_folder_path in test_paths:
        for file_path in test_folder_path.iterdir():
            assert not 'dupe' in str(file_path)

    print('Remove test passed!')


def cleanup_test():
    for test_folder_path in test_paths:
        for file_path in test_folder_path.iterdir():
            file_path.unlink()
        test_folder_path.rmdir()

    base_path = Path(base_pathname)
    for file_path in base_path.iterdir():
        file_path.unlink()

    base_path.rmdir()

    print('Test data removed.')


if __name__ == '__main__':
    setup_test()

    identify(
        path_names=[str(p) for p in test_paths],
        identify_pathname=identify_pathname,
        verbose=True
    )
    verify_identify()

    remove(
        dry_run=False,
        identify_pathname=identify_pathname,
        verbose=True
    )
    verify_remove()

    cleanup_test()
