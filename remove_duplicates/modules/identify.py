from collections import defaultdict
import csv
import datetime
import hashlib
import logging

from .validate_paths import validate_csv, validate_passed_path_list


def identify(passed_path_names,
             outfile,
             recurse=False,
             progress=False):
    hashed_files_seen = defaultdict(list)
    all_duplicate_names = set()
    files_processed = 0

    all_file_paths, total_filecount, progress_init_time = validate_passed_path_list(passed_path_names,
                                                                                   recurse)
    # Identify!
    for files_processed_count, file_path in enumerate(all_file_paths, start=1):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buf = file.read()
        hasher.update(buf)
        file_hash = hasher.hexdigest()

        # todo verify
        hashed_files_seen[file_hash].append(file_path)
        if len(hashed_files_seen[file_hash]) != 1:
            all_duplicate_names = f'{(str(p) for p in hashed_files_seen[file_hash])}'
            logging.debug(f'Found duplicates: {all_duplicate_names}')

        if progress:
            progress_log(task_name=f'Identify Duplicates',
                         processed_files=files_processed_count,
                         total_files=total_filecount)

    # todo verify
    # logging.info(f'Files with copies found: {len(hashed_files_seen)}')
    logging.debug(f'Writing identified duplicates: {str(outfile)}')

    with open(outfile, 'w', newline='') as csvfile:
        dupe_writer = csv.writer(csvfile)
        for line in all_duplicate_names:
            dupe_writer.writerow(line)

    return files_processed
