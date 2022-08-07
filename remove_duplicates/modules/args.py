import argparse
import inspect


def parse_args():
    parser = argparse.ArgumentParser(description='Remove duplicate files across paths.')
    parser.add_argument('paths', type=str, nargs='+', metavar='~/path1 ~/path2',
                        help='paths to deduplicate')
    parser.add_argument('--dry_run', '-d', action=argparse.BooleanOptionalAction, default=False,
                        help=inspect.cleandoc('''
                            Skips file removal. You will be able to view and verify duplicates found with verbose mode or by
                            providing viewing the output csv file.
    
                            Running this command with verbose mode on will log the removal steps. Running it with verbose 
                            off completely skips removal.
    
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
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help=inspect.cleandoc('''
                            Logs additional information while running. You can add an additional 
                            '-v' or use '-vv' for increased logging.
                            '''))

    return parser.parse_args()
