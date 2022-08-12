import datetime
import logging
from pathlib import Path
import tempfile


def validate_passed_path_list(path_names, recurse=False):
    logging.info(f'Processing passed paths into work list: {path_names}')

    all_dir_paths, all_file_paths = [], []

    if not path_names:
        raise ValueError('You must pass at least one path.')
    elif isinstance(path_names, str) or isinstance(path_names, list):
        all_dir_paths = [Path(dir_name).expanduser() for dir_name in path_names]

    for dir_path in all_dir_paths:
        if not dir_path.exists():
            error_message = 'Cannot find path:'
            logging.error(error_message)
            raise ValueError(error_message, dir_path)
        elif dir_path.is_file():
            error_message = 'Not a directory:'
            logging.error(error_message)
            raise ValueError(error_message, dir_path)

        for file_path in dir_path.iterdir():
            if file_path.is_file():
                all_file_paths.append(file_path)
            else:
                if recurse:
                    logging.debug(f'Found sub-directory: {file_path}/')
                    all_dir_paths.append(file_path)

    # all_dir_paths, total_filecount = len(all_dir_paths), len(all_file_paths)
    logging.info(f'Found {len(all_file_paths)} files to hash check in {len(all_dir_paths)} directories.')

    return all_file_paths


def validate_csv(identify_pathname):
    if not identify_pathname:
        identify_file = tempfile.NamedTemporaryFile(delete=False)
        identify_pathname = identify_file.name

    # Validate Identify/Outfile Path
    identify_path = Path(identify_pathname)
    if not identify_path.parent.exists():
        error_message = 'Cannot find path for identity file:'
        logging.error(error_message)
        raise ValueError(error_message, identify_path.parent)

    identify_path.touch(exist_ok=True)
    return identify_path
