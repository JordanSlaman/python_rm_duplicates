import argparse
from collections import defaultdict
import datetime
import csv
import hashlib
import inspect
import logging
from pathlib import Path
import tempfile


import remove_duplicates.modules.args

# Verbosity
# LOG_LEVELS = ['ERROR', 'INFO', 'DEBUG', 'NOTSET']
# DEFAULT_LOG_LEVEL = LOG_LEVELS.index('ERROR')
#
# # Progress
# PROGRESS_GLOBALS = {
#     'total_start_datetime': datetime.datetime.now(),
#     'last_progress_datetime': datetime.datetime.now(),
#     'last_progress_percentage': 0.0,
#     'last_progress_percentage_int': 0,
#
#     'threshold_minutes_to_report': 1,
#     'threshold_percentage_to_report': 5,
#
#     'tasks': defaultdict(dict)
# }


# def validate_and_build_paths(path_names, recurse=False):
#     progress_init_time = datetime.datetime.now()
#     logging.info(f'Processing passed paths into work list: {path_names}')
#
#     all_dir_paths, all_file_paths = [], []
#
#     if not path_names:
#         raise ValueError('You must pass at least one path.')
#     elif isinstance(path_names, str) or isinstance(path_names, list):
#         all_dir_paths = [Path(dir_name).expanduser() for dir_name in path_names]
#
#     for dir_path in all_dir_paths:
#         if not dir_path.exists():
#             error_message = 'Cannot find path:'
#             logging.error(error_message)
#             raise ValueError(error_message, dir_path)
#         elif dir_path.is_file():
#             error_message = 'Not a directory:'
#             logging.error(error_message)
#             raise ValueError(error_message, dir_path)
#
#         for file_path in dir_path.iterdir():
#             if file_path.is_file():
#                 all_file_paths.append(file_path)
#             else:
#                 if recurse:
#                     logging.debug(f'Found sub-directory: {file_path}/')
#                     all_dir_paths.append(file_path)
#
#     all_dir_paths, total_filecount = len(all_dir_paths), len(all_file_paths)
#     logging.info(f'Found {total_filecount} files to hash check in {all_dir_paths} directories.')
#
#     return all_file_paths, total_filecount, progress_init_time
#
#
# def validate_identify_csv_path(identify_pathname):
#     if not identify_pathname:
#         identify_file = tempfile.NamedTemporaryFile(delete=False)
#         identify_pathname = identify_file.name
#
#     # Validate Identify/Outfile Path
#     identify_path = Path(identify_pathname)
#     if not identify_path.parent.exists():
#         error_message = 'Cannot find path for identity file:'
#         logging.error(error_message)
#         raise ValueError(error_message, identify_path.parent)
#
#     identify_path.touch(exist_ok=True)
#     return identify_path


# def human_timedelta(delta):
#     d = delta.days
#     h, s = divmod(delta.seconds, 3600)
#     m, s = divmod(s, 60)
#
#     if not any((d, h, m, s)):
#         return '0 seconds'
#
#     labels = ['day', 'hour', 'minute', 'second']
#     dhms = ['%s %s%s' % (i, lbl, 's' if i != 1 else '') for i, lbl in zip([d, h, m, s], labels)]
#     for start in range(len(dhms)):
#         if not dhms[start].startswith('0'):
#             break
#     for end in range(len(dhms) - 1, -1, -1):
#         if not dhms[end].startswith('0'):
#             return ', '.join(dhms[start:end + 1])


# def progress_log(task_name, processed_files, total_files):
#     threshold_minutes_to_report = PROGRESS_GLOBALS['threshold_minutes_to_report']
#
#     # Total Progress Elapsed
#
#     task_progress_global = PROGRESS_GLOBALS['tasks'].get('task_name', default=task_name)
#     last_progress_timedelta = task_progress_global.get('last_progress_timedelta', default=datetime.timedelta())
#
#     if last_progress_timedelta == datetime.timedelta(minutes=PROGRESS_GLOBALS['threshold_minutes_to_report']):
#         logging.info(f'Elapsed task time: {human_timedelta(last_progress_timedelta)}')
#     #     PROGRESS_GLOBALS['last_progress_datetime'] = datetime.datetime.now()
#
#     # todo wat
#     # Total Progress Percentage
#
#     last_progress_percentage = PROGRESS_GLOBALS['last_progress_percentage']
#
#     try:
#         last_progress_percentage = (processed_files / last_progress_percentage) * 100
#     except ZeroDivisionError:
#         last_progress_percentage_int = 0
#     else:
#         last_progress_percentage_int = int(last_progress_percentage)
#
#     if last_progress_percentage_int == PROGRESS_GLOBALS['threshold_percentage_to_report']:
#         logging.info(f'{task_name}: {last_progress_percentage_int :.2%}')
#
#     # - Elapsed task time: {human_timedelta(elapsed)}
#     st = PROGRESS_GLOBALS['total_start_datetime']
#     lt = PROGRESS_GLOBALS['last_progress_datetime']

    x = 3
    # elapsed_total =
    # last_delta = datetime.datetime.now() - start_datetime

    # just log progress every x minutes?
    # print(elapsed)
    # if elapsed:
    #     pass

    # elapsed_since_last_progress =

    # report_progress = threshold_percent_to_report > last_progress_percentage
    #     last_progress_percentage > threshold_minutes_to_report

    # if report_progress:
    #     last_progress_datetime = datetime.datetime.now()
    #     last_progress_percentage = last_progress_percentage
    #     print(f'{task_name}: {.2%} - Elapsed task time: {human_timedelta(elapsed)}')


# def identify(passed_path_names,
#              outfile,
#              recurse=False,
#              progress=False):
#     hashed_files_seen = defaultdict(list)
#     all_duplicate_names = set()
#     files_processed = 0
#
#     all_file_paths, total_filecount, progress_init_time = validate_and_build_paths(passed_path_names,
#                                                                                    recurse)
#     # Identify!
#     for files_processed_count, file_path in enumerate(all_file_paths, start=1):
#         hasher = hashlib.md5()
#         with open(file_path, 'rb') as file:
#             buf = file.read()
#         hasher.update(buf)
#         file_hash = hasher.hexdigest()
#
#         # todo verify
#         hashed_files_seen[file_hash].append(file_path)
#         if len(hashed_files_seen[file_hash]) != 1:
#             all_duplicate_names = f'{(str(p) for p in hashed_files_seen[file_hash])}'
#             logging.debug(f'Found duplicates: {all_duplicate_names}')
#
#         if progress:
#             progress_log(task_name=f'Identify Duplicates',
#                          processed_files=files_processed_count,
#                          total_files=total_filecount)
#
#     # todo verify
#     # logging.info(f'Files with copies found: {len(hashed_files_seen)}')
#     logging.debug(f'Writing identified duplicates: {str(outfile)}')
#
#     with open(outfile, 'w', newline='') as csvfile:
#         dupe_writer = csv.writer(csvfile)
#         for line in all_duplicate_names:
#             dupe_writer.writerow(line)
#
#     return files_processed


# def remove(infile,
#            dry_run=False,
#            rm_empty_dirs=True,
#            progress=False):
#     files_removed = 0
#     paths_to_remove = set()
#     directories_seen = set()
#     # progress_init = datetime.datetime.now()
#
#     logging.info(f'Removing found duplicates from identified duplicates file: {infile}')
#
#     with open(infile, newline='') as csvfile:
#         identity_reader = csv.reader(csvfile)
#         for row in identity_reader:
#             for filename in row[1:]:
#
#                 file_path = Path(filename)
#                 if file_path.exists():
#                     paths_to_remove.add(file_path)
#
#                 if rm_empty_dirs:
#                     directories_seen.add(file_path.parent)
#
#     progress_filecount = len(paths_to_remove)
#
#     for file_path in paths_to_remove:
#         logging.info(f'Unlinking file: {file_path}{" - Dry Run!" if dry_run else ""}')
#
#         if not dry_run:
#             file_path.unlink()
#             files_removed += 1
#             if rm_empty_dirs:
#                 file_parent_dir = file_path.parent
#                 try:
#                     file_parent_dir.rmdir()
#                 except OSError:
#                     pass
#
#         if progress:
#             progress_log(task_name=f'Removing Duplicates',
#                          processed_files=files_removed,
#                          total_files=progress_filecount,
#                          last_progress_percentage=0)
#
#     logging.info(f'Removed {files_removed} files total.')


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Remove duplicate files across paths.')
    # parser.add_argument('paths', type=str, nargs='+', metavar='~/path1 ~/path2',
    #                     help='paths to deduplicate')
    # parser.add_argument('--dry_run', '-d', action=argparse.BooleanOptionalAction, default=False,
    #                     help=inspect.cleandoc('''
    #                         Skips file removal. You will be able to view and verify duplicates found with verbose mode or by
    #                         providing viewing the output csv file.
    #
    #                         Running this command with verbose mode on will log the removal steps. Running it with verbose
    #                         off completely skips removal.
    #
    #                         Duplicates found in the outfile are removed from right to left.
    #                         Only the first filepath in the list will be kept, so the order you pass your paths is important.
    #                         '''))
    # parser.add_argument('--found_duplicates_csv_filepath', '-f', type=str, metavar='./duplicates_found.csv',
    #                     default=None,
    #                     help=inspect.cleandoc('''
    #                             Pass in a filepath to output identified duplicates to.
    #                             The output format is a .csv of duplicated paths.
    #                             Only the first row (first file found in path order.) is preserved.
    #                             Removal will proceed using this file unless "--dry_run" is specified.
    #                             '''))
    # parser.add_argument('--skip_identification', '-s', action=argparse.BooleanOptionalAction, default=False,
    #                     help=inspect.cleandoc('''
    #                         Uses the file provided by --found_duplicates_csv_filepath to process removals.
    #                         This saves a lot of time iterating and hashing all files in the provided paths.
    #                         '''))
    # parser.add_argument('--recurse', '-r', action=argparse.BooleanOptionalAction, default=False,
    #                     help='recurse into subdirectories')
    # parser.add_argument('--keep_empty_subdirectories', '-k', action=argparse.BooleanOptionalAction, default=False,
    #                     help='Will not delete a directory or if it is empty after file deduplication.')
    # parser.add_argument('--progress', '-p', action=argparse.BooleanOptionalAction, default=False,
    #                     help=inspect.cleandoc('''
    #                         Shows a crude form of progress for both steps, will add
    #                         additional time to the overall operation as it needs to iterate over the paths.
    #                         '''))
    # parser.add_argument('--verbose', '-v', action='count', default=0,
    #                     help=inspect.cleandoc('''
    #                         Logs additional information while running. You can add an additional
    #                         '-v' or use '-vv' for increased logging.
    #                         '''))
    #
    # args = parser.parse_args()

    # identified_csv_filepath = validate_identify_csv_path(args.found_duplicates_csv_filepath)

    # if args.verbose:
    #     log_level_name = LOG_LEVELS[args.verbose]
    #     logging.getLogger().setLevel(log_level_name)
    #     logging.debug(f"Beginning deduplication! Logging verbosity = {log_level_name}")

    # if not args.skip_identification:
    #     identify(args.paths,
    #              outfile=identified_csv_filepath,
    #              recurse=args.recurse,
    #              progress=args.progress)
    # else:
    # #     logging.info(f"Skipping deduplication - Will remove from {identified_csv_filepath}")
    #
    #     if not args.found_duplicates_csv_filepath:
    #         Path(identified_csv_filepath).unlink()  # deletes temporary directory
    #
    # skip_removal = args.dry_run and not args.verbose
    # if not skip_removal:
    #     remove(infile=identified_csv_filepath,
    #            dry_run=args.dry_run,
    #            rm_empty_dirs=not args.keep_empty_subdirectories,
    #            progress=args.progress)
    #
    # script_elapsed = datetime.datetime.now() - PROGRESS_GLOBALS['total_start_datetime']
    # logging.debug(f'Done! - Elapsed total time: {human_timedelta(script_elapsed)}')
