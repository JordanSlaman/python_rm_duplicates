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
usage: rm_duplicates.py [-h] [--dry_run | --no-dry_run | -d] [--outfile OUTFILE] [--cleanup_outfile | --no-cleanup_outfile | -c]
                        [--infile INFILE] [--recurse | --no-recurse | -r] [--keep_empty_subdirs | --no-keep_empty_subdirs | -k]
                        [--progress | --no-progress | -p] [--verbose | --no-verbose | -v]
                        ~/path1 ~/path2 [~/path1 ~/path2 ...]

Remove duplicate files across paths.

positional arguments:
  ~/path1 ~/path2       paths to deduplicate

options:
  -h, --help            show this help message and exit
  --dry_run, --no-dry_run, -d
                        Skips file removal. You will be able to view and verify duplicates found with verbose mode or by providing
                        viewing the output csv file. Duplicates found in the outfile are removed from right to left. Only the first
                        filepath in the list will be kept, so the order you pass your paths is important. (default: False)
  --outfile OUTFILE, -o OUTFILE
                        Pass in a filepath other than "./found_duplicates.csv"
  --cleanup_outfile, --no-cleanup_outfile, -c
                        Will remove the outfile from the identify step if flagged. (default: False)
  --infile INFILE, -i INFILE
                        Pass in a filepath to process removals from. This option will skip the identification step.
  --recurse, --no-recurse, -r
                        recurse into subdirectories (default: False)
  --keep_empty_subdirs, --no-keep_empty_subdirs, -k
                        Will not delete a directory or if it is empty after file deduplication. (default: False)
  --progress, --no-progress, -p
                        Shows a crude form of progress for both steps, will add additional time to the overall operation as it needs
                        to iterate over the paths. (default: False)
  --verbose, --no-verbose, -v
                        Logs additional information while running. (default: False)
```
