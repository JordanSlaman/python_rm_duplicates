import argparse
from collections import defaultdict
import csv
import hashlib
from pathlib import Path

# argparse?
# recursive?

identify_outfile_pathname = './found.csv'


def identify(path_names=None,
             identify_pathname=identify_outfile_pathname,
             recurse=False,
             verbose=False):
    search_paths = []
    files_seen = defaultdict(list)

    # Validate Path List
    if not path_names:
        raise ValueError('You must pass at least one path.')
    elif isinstance(path_names, str):
        path_names = [path_names]

    for path_name in path_names:
        folder_path = Path(path_name)
        if not folder_path.exists():
            raise ValueError('Cannot find path:', path_name)
        else:
            search_paths.append(folder_path)

    # Validate Identify Outfile Path
    identify_path = Path(identify_pathname)
    if identify_path:
        if not identify_path.parent.exists():
            raise ValueError('Cannot find path for identity outfile:', identify_path.parent)
    if verbose:
        print('Identifying duplicates in paths:', path_names)

    for search_path in search_paths:
        for files_processed, file_path in enumerate(search_path.iterdir(), start=1):

            if file_path.is_file():
                hasher = hashlib.md5()
                with open(file_path, 'rb') as file:
                    buf = file.read()
                hasher.update(buf)
                file_hash = hasher.hexdigest()

                files_seen[file_hash].append(file_path)

                if len(files_seen[file_hash]) != 1:
                    if verbose:
                        print('Found duplicate:', files_seen[file_hash])
            else:
                if verbose:
                    print('Found directory:', file_path)

                if recurse:
                    if verbose:
                        print('Adding directory to paths.')
                    search_paths.append(file_path)

            if verbose and files_processed % 100 == 0:
                print(f'Processed {files_processed} files from {search_path}.')

        else:
            if verbose:
                print(f'Processed {files_processed} total files from {search_path}.')

    duplicate_list = [v for v in files_seen.values() if len(v) != 1]
    if verbose:
        print(f'Files with copies found:', len(duplicate_list))

    if verbose:
        print('Writing identified duplicates:', identify_path)

    with open(identify_path, 'w', newline='') as csvfile:
        dupe_writer = csv.writer(csvfile)
        for line in duplicate_list:
            dupe_writer.writerow(line)


def remove(dry_run=False,
           identify_pathname=identify_outfile_pathname,
           verbose=False):
    files_removed = 0

    if verbose:
        print('Removing duplicates from:', identify_pathname)

    identify_path = Path(identify_pathname)
    if not identify_path.exists():
        raise ValueError('Cannot find path for identity outfile:', identify_path.parent)

    with open(identify_path, newline='') as csvfile:
        identity_reader = csv.reader(csvfile)
        for row in identity_reader:
            for filename in row[1:]:

                file_path = Path(filename)
                if file_path.exists():
                    if verbose:
                        print('Unlinking file:', file_path)

                    if not dry_run:
                        file_path.unlink()
                        files_removed += 1

                    if verbose and files_removed % 100 == 0:
                        print(f'Removed {files_removed} files...')

    if verbose:
        print(f'Removed {files_removed} files total.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove duplicate files across paths.')
    parser.add_argument('paths', type=str, nargs='+', metavar='~/path1 ~/path2',
                        help='paths to deduplicate')
    parser.add_argument('--recurse', '-r', action=argparse.BooleanOptionalAction, default=False,
                        help='recurse into subdirectories')
    parser.add_argument('--dry_run', '-d', action=argparse.BooleanOptionalAction, default=False,
                        help='do not remove files')
    parser.add_argument('--verbose', '-v', action=argparse.BooleanOptionalAction, default=False,
                        help='Logs additional information while running.')

    args = parser.parse_args()

    identify(path_names=args.paths, recurse=args.recurse, verbose=args.verbose)
    remove(dry_run=args.dry_run, verbose=args.verbose)
