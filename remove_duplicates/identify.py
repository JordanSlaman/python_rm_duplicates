from collections import defaultdict
import csv
import hashlib
import logging

from progress import progress_log
from validate_paths import validate_csv, validate_passed_path_list


def identify(search_paths,
             outfile,
             recurse=False):
    all_hashed_file_paths_seen = defaultdict(set)  # Key: hash, Value: set of Paths
    all_duplicate_paths = defaultdict(set)  # Key: hash, Value: set of Paths
    # all_duplicate_names = defaultdict(set)  # Key: hash, Value: set of file names

    progress_log(task_name=f'identify')

    # Identify!
    for files_processed_count, file_path in enumerate(search_paths, start=1):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buf = file.read()
        hasher.update(buf)
        file_hash = hasher.hexdigest()

        all_hashed_file_paths_seen[file_hash].add(file_path)
        current_file_duplicate_paths = all_hashed_file_paths_seen[file_hash]

        # Is Dupe
        if len(current_file_duplicate_paths) != 1:
            all_duplicate_paths[file_hash].add(file_path)

        progress_log(task_name='identify',
                     qty_processed=files_processed_count)

    logging.debug(f'Writing identified duplicates: {str(outfile)}')
    duplicate_list = [v for v in all_hashed_file_paths_seen.values() if len(v) != 1]
    with open(outfile, 'w', newline='') as csvfile:
        dupe_writer = csv.writer(csvfile)
        for line in duplicate_list:
            dupe_writer.writerow(line)

    x=3
    # all_duplicate_names = [str(p) for p in all_duplicate_paths.values()]
    # logging.debug(f'Found duplicates: {all_duplicate_names}')
    # logging.info(f'Files with copies found: {len(all_hashed_file_paths_seen)}')
