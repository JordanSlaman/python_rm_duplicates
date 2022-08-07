import datetime
import logging
from pathlib import Path
import sys

from modules import *

if __name__ == '__main__':
    print(sys.argv)

    print(parse_args())
    args = parse_args()

    init_loglevel(verbosity=args.verbosity)
    progress(enabled=args.progress)

    identified_csv_filepath = validate_csv(args.found_duplicates_csv_filepath)

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

    script_elapsed = datetime.datetime.now() - PROGRESS_TASKS['total']['start_datetime']
    logging.debug(f'Done! - Elapsed total time: {human_timedelta(script_elapsed)}')

    b = 3

    all_file_paths, total_filecount, progress_init_time = validate_passed_path_list(passed_path_names,
                                                                                    recurse)

    identify(
        args.
    )
