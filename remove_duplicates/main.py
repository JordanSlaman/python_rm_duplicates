import logging
from pathlib import Path

from args import parse_args
from identify import identify
from progress import init_progress, progress_log, log_done
from remove import remove
from validate_paths import validate_csv, validate_passed_path_list
from verbosity import init_loglevel


def main():
    args = parse_args()
    init_loglevel(verbosity=args.verbose)
    all_file_paths = validate_passed_path_list(path_names=args.paths, recurse=args.recurse)
    init_progress(enabled=args.progress, total_filecount=len(all_file_paths))

    # Identify
    identified_csv_filepath = validate_csv(args.found_duplicates_csv_filepath)

    if not args.skip_identification:
        identify(search_paths=all_file_paths,
                 outfile=identified_csv_filepath,
                 recurse=args.recurse)
    else:
        logging.info(f"Skipping deduplication - Will remove from {identified_csv_filepath}")

    # todo wazzis
    if not args.found_duplicates_csv_filepath:
        Path(identified_csv_filepath).unlink()  # deletes temporary directory

    # Remove
    skip_removal = args.dry_run and not args.verbose
    if not skip_removal:
        remove(infile=identified_csv_filepath,
               dry_run=args.dry_run,
               rm_empty_dirs=not args.keep_empty_subdirectories)

    # todo unnecessary? use progress normal
    log_done()


if __name__ == "__main__":
    main()
