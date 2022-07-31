import argparse
from collections import defaultdict
import datetime
import csv
import hashlib
import inspect
import logging
from pathlib import Path
import tempfile


def validate_and_return_passed_search_paths(path_names):
    search_paths = []

    if not path_names:
        raise ValueError('You must pass at least one path.')
    elif isinstance(path_names, str):
        path_names = [path_names]

    for path_name in path_names:
        folder_path = Path(path_name).expanduser()

        if not folder_path.exists():
            raise ValueError('Cannot find path:', path_name)
        else:
            search_paths.append(folder_path)

    return search_paths


def validate_identify_csv_path(identify_pathname):
    if not identify_pathname:
        identify_file = tempfile.NamedTemporaryFile(delete=False)
        identify_pathname = identify_file.name

    # Validate Identify/Outfile Path
    identify_path = Path(identify_pathname)
    if not identify_path.parent.exists():
        raise ValueError('Cannot find path for identity file:', identify_path.parent)

    identify_path.touch(exist_ok=True)
    return identify_path


def human_timedelta(delta):
    d = delta.days
    h, s = divmod(delta.seconds, 3600)
    m, s = divmod(s, 60)

    if not any((d, h, m, s)):
        return '0 seconds'

    labels = ['day', 'hour', 'minute', 'second']
    dhms = ['%s %s%s' % (i, lbl, 's' if i != 1 else '') for i, lbl in zip([d, h, m, s], labels)]
    for start in range(len(dhms)):
        if not dhms[start].startswith('0'):
            break
    for end in range(len(dhms) - 1, -1, -1):
        if not dhms[end].startswith('0'):
            return ', '.join(dhms[start:end + 1])


def progress_log(task_name, processed, total, start_datetime):
    percentage = (processed / total) * 100
    elapsed = datetime.datetime.now() - start_datetime

    if int(percentage) % 10 == 0:
        print(f'{task_name}: {processed / total:.2%} - Elapsed task time: {human_timedelta(elapsed)}')


def progress_count_files(passed_paths, recurse=False):
    # Progress indicator iteration!
    progress_filecount = 0

    for search_path in passed_paths:
        for processed_paths, file_path in enumerate(search_path.iterdir(), start=1):

            if file_path.is_file():
                progress_filecount += 1
            else:
                if recurse:
                    passed_paths.append(file_path)
        logging.info(f'Found {progress_filecount} files to hash check.')

    return progress_filecount


def identify(passed_path_names,
             outfile,
             recurse=False,
             progress=False):
    files_seen = defaultdict(list)
    files_processed = 0

    progress_filecount = 0
    progress_init = datetime.datetime.now()

    search_paths = validate_and_return_passed_search_paths(passed_path_names)

    if progress:
        # Track progress for Identify
        progress_filecount = progress_count_files(search_paths, recurse=recurse)

    # Identify!
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
                    logging.info('Found duplicate:', *(str(p) for p in files_seen[file_hash]))
            else:
                logging.info('Found directory:', file_path)

                if recurse:
                    logging.info('Adding directory to paths.')
                    search_paths.append(file_path)

            if progress:
                progress_log(task_name=f'Identify Duplicates in {search_path}',
                             processed=files_processed,
                             total=progress_filecount,
                             start_datetime=progress_init)

        else:
            logging.info(f'Processed {files_processed} total files from {search_path}')

    duplicate_list = [v for v in files_seen.values() if len(v) != 1]
    logging.info(f'Files with copies found: {len(duplicate_list)}')

    logging.info('Writing identified duplicates:', str(outfile))

    with open(outfile, 'w', newline='') as csvfile:
        dupe_writer = csv.writer(csvfile)
        for line in duplicate_list:
            dupe_writer.writerow(line)

    return files_processed


def remove(infile,
           dry_run=False,
           rm_empty_dirs=True,
           progress=False):
    files_removed = 0
    paths_to_remove = set()
    directories_seen = set()
    progress_init = datetime.datetime.now()

    logging.info(f'Removing found duplicates from identified duplicates file: {infile}')

    with open(infile, newline='') as csvfile:
        identity_reader = csv.reader(csvfile)
        for row in identity_reader:
            for filename in row[1:]:

                file_path = Path(filename)
                if file_path.exists():
                    paths_to_remove.add(file_path)

                if rm_empty_dirs:
                    directories_seen.add(file_path.parent)

    progress_filecount = len(paths_to_remove)

    for file_path in paths_to_remove:
        logging.info(f'Unlinking file: {file_path}{" - Dry Run!" if dry_run else ""}')

        if not dry_run:
            file_path.unlink()
            files_removed += 1
            if rm_empty_dirs:
                file_parent_dir = file_path.parent
                try:
                    file_parent_dir.rmdir()
                except OSError:
                    pass

        if progress:
            progress_log(task_name=f'Removing Duplicates',
                         processed=files_removed,
                         total=progress_filecount,
                         start_datetime=progress_init)

    logging.info(f'Removed {files_removed} files total.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove duplicate files across paths.')
    parser.add_argument('paths', type=str, nargs='+', metavar='~/path1 ~/path2',
                        help='paths to deduplicate')
    parser.add_argument('--dry_run', '-d', action=argparse.BooleanOptionalAction, default=False,
                        help=inspect.cleandoc('''
                        Skips file removal. You will be able to view and verify duplicates found with verbose mode or by
                        providing viewing the output csv file.
                        
                        Running this command with verbose mode on will log the removal steps. Running it with verbose off
                        completely skips removal.
                                                
                        Duplicates found in the outfile are removed from right to left.
                        Only the first filepath in the list will be kept, so the order you pass your paths is important.
                        '''))
    parser.add_argument('--found_duplicates_csv_filepath', '-f', type=str, metavar='./duplicates_found.csv',
                        default=None,
                        help=inspect.cleandoc('''
                            Pass in a filepath to output identified duplicates to.
                            The output format is a .csv of duplicated paths.
                            Only the first row (first file found in path order.) is preserved.
                            Removal will proceed using this file unless "--dry_run" is specified.
                            '''))
    parser.add_argument('--skip_identification', '-s', action=argparse.BooleanOptionalAction, default=False,
                        help=inspect.cleandoc('''
                        Uses the file provided by --found_duplicates_csv_filepath to process removals.
                        This saves a lot of time iterating and hashing all files in the provided paths.
                        '''))
    parser.add_argument('--recurse', '-r', action=argparse.BooleanOptionalAction, default=False,
                        help='recurse into subdirectories')
    parser.add_argument('--keep_empty_subdirectories', '-k', action=argparse.BooleanOptionalAction, default=False,
                        help='Will not delete a directory or if it is empty after file deduplication.')
    parser.add_argument('--progress', '-p', action=argparse.BooleanOptionalAction, default=False,
                        help=inspect.cleandoc('''
                        Shows a crude form of progress for both steps, will add
                        additional time to the overall operation as it needs to iterate over the paths.
                        '''))
    parser.add_argument('--verbose', '-v', action=argparse.BooleanOptionalAction, default=False,
                        help='Logs additional information while running.')

    args = parser.parse_args()
    script_start = datetime.datetime.now()
    identified_csv_filepath = validate_identify_csv_path(args.found_duplicates_csv_filepath)

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("Beginning deduplication!")

    if not args.skip_identification:
        identify(args.paths,
                 outfile=identified_csv_filepath,
                 recurse=args.recurse,
                 progress=args.progress)
    else:
        logging.info(f"Skipping deduplication - Will remove from {identified_csv_filepath}")

        if not args.found_duplicates_csv_filepath:
            Path(identified_csv_filepath).unlink()  # deletes temporary directory

    skip_removal = args.dry_run and not args.verbose
    if not skip_removal:
        remove(infile=identified_csv_filepath,
               dry_run=args.dry_run,
               rm_empty_dirs=not args.keep_empty_subdirectories,
               progress=args.progress)

    if args.verbose:
        script_elapsed = datetime.datetime.now() - script_start
        logging.info(f'Done! - Elapsed total time: {human_timedelta(script_elapsed)}')
