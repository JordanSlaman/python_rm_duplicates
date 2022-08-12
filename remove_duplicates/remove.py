import csv
import logging
from pathlib import Path

from progress import progress_log


def remove(infile,
           dry_run=False,
           rm_empty_dirs=True):
    files_removed = 0
    paths_to_remove = set()
    directories_seen = set()

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

        # todo
        # total files != dupes progress...
        progress_log(task_name=f'remove', qty_processed=files_removed)
        # processed_files=files_removed,
        # total_files=progress_filecount,
        # last_progress_percentage=0)

    logging.info(f'Removed {files_removed} files total.')
