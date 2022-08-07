# Python Remove Duplicate Files

## About

This is a pure python script to remove files from one or more directories.

Filenames are not used to compare files.
The leftmost paths take precedent, so the copy you wish to keep should be in the first path you pass.

I wrote it because I had made a backup of my phone photos in dropbox, and another in Google Drive, and then I bought a
NAS and decided to cut out the other services.
The NAS also backs up my phone photos, so I had three copies of some things.

There's a file `test.py` you can read and execute.
You could comment out the cleanup step and verify assumptions yourself before running this on data you care about.

## Requirements & Execution

Python 3.9 and above.

I recommend [asdf-vm](https://asdf-vm.com/) to manage local python versions, or use what you're comfortable with.

`python rm_duplicates.py "~/Photos/Jordan's Phone" "/Volumes/old_backup/photos" -v -r -p`

## Options

`python rm_duplicates.py --help`

```
usage: rm_duplicates.py [-h] [--dry_run | --no-dry_run | -d] [--found_duplicates_csv_filepath ./duplicates_found.csv] [--skip_identification | --no-skip_identification | -s] [--recurse | --no-recurse | -r]
                        [--keep_empty_subdirectories | --no-keep_empty_subdirectories | -k] [--progress | --no-progress | -p] [--verbose | --no-verbose | -v]
                        ~/path1 ~/path2 [~/path1 ~/path2 ...]

Remove duplicate files across paths.

positional arguments:
  ~/path1 ~/path2       paths to deduplicate

options:
  -h, --help            show this help message and exit
  --dry_run, --no-dry_run, -d
                        Skips file removal. You will be able to view and verify duplicates found with verbose mode or by providing viewing the output csv file. Running this command with verbose mode on will
                        log the removal steps. Running it with verbose off completely skips removal. Duplicates found in the outfile are removed from right to left. Only the first filepath in the list will be
                        kept, so the order you pass your paths is important. (default: False)
  --found_duplicates_csv_filepath ./duplicates_found.csv, -f ./duplicates_found.csv
                        Pass in a filepath to output identified duplicates to. The output format is a .csv of duplicated paths. Only the first row (first file found in path order.) is preserved. Removal will
                        proceed using this file unless "--dry_run" is specified.
  --skip_identification, --no-skip_identification, -s
                        Uses the file provided by --found_duplicates_csv_filepath to process removals. This saves a lot of time iterating and hashing all files in the provided paths. (default: False)
  --recurse, --no-recurse, -r
                        recurse into subdirectories (default: False)
  --keep_empty_subdirectories, --no-keep_empty_subdirectories, -k
                        Will not delete a directory or if it is empty after file deduplication. (default: False)
  --progress, --no-progress, -p
                        Shows a crude form of progress for both steps, will add additional time to the overall operation as it needs to iterate over the paths. (default: False)
  --verbose, --no-verbose, -v
                        Logs additional information while running. (default: False)
```

# Advanced Usage - Review & Safety

This script contains 2 primary steps.

1. Identify
This step walks the paths provided in order and hashes all the files found. (and optionally continues into subdirectories with `--recurse`)
It saves the identified paths to a .csv in a temporary folder if unspecified.

You can provide a filepath for your own .csv to review before you commit to a removal.
You would need to also use the `--dry_run` flag for this to prevent the 

Relevant options:
- paths (positional)
- `-r` recurse
- `-p` progress
- `-v` verbose
- `-f` found_duplicates_csv_filepath


2. Remove

Running this command with verbose mode on will log the removal steps. Running it with verbose off completely skips removal.

- `-d` dry_run
- `-r` recurse
- `-k` keep_empty_subdirectories
- `-p` progress
- `-v` verbose
- `-f` found_duplicates_csv_filepath


## Examples

### Identify to file
> -f ./duplicates.csv -r -p -d "/Volumes/Backup/Photos/Jordan's Phone" "~/Jordan Dropbox/media/From Phone"

### Remove from file
> -f ./duplicates.csv -r -p -s "/Volumes/Backup/Photos/Jordan's Phone" "~/Jordan Dropbox/media/From Phone"
