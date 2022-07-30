import csv
from pathlib import Path
import os

from rm_duplicates import identify, remove

base_pathname = os.path.realpath(__file__).rstrip('.py') + '/'
identify_path = base_pathname + 'test_idenfify.csv'

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
    },
    'path3': {  # all dupes, should be preserved with keep_empty_dirs
        'first_dupe4': 'coffee',
        'first_dupe5': 'coffee',
        'second_dupe2': 'bagel',
        'third_dupe': 'tea'
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
    with open(identify_path, newline='') as csvfile:
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
        [str(p) for p in test_paths],
        outfile=identify_path,
        progress=True
    )
    verify_identify()

    remove(
        infile=identify_path,
        dry_run=False,
        rm_empty_dirs=False,
        progress=True
    )
    verify_remove()

    cleanup_test()

# TODO: Testing...
'''
 - use unittest
 - write test for each arg
 - test for recurse flag
    if isinstance(dict) in fixture?
 - verify tempdir & cleanup works
'''
