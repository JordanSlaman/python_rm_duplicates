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

There is also a `dry_run` flag that will not delete the files.
If you have many files and the identification/hashing process takes a long time you can run a dry_run, verify the
outfile `./found.csv` and run only the removal by commenting out the identify command.

## Requirements & Execution

Python 3.9 and above.

I recommend [asdf-vm](https://asdf-vm.com/) to manage local python versions, or use what you're comfortable with.

`python rm_duplicates.py ~/path1/ ~/path2`

## Options

`python rm_duplicates.py --help`

```
usage: rm_duplicates.py [-h] [--recurse | --no-recurse | -r] [--dry_run | --no-dry_run | -d] [--verbose | --no-verbose | -v]
                        ~/path1 ~/path2 [~/path1 ~/path2 ...]

Remove duplicate files across paths.

positional arguments:
  ~/path1 ~/path2       paths to deduplicate

optional arguments:
  -h, --help            show this help message and exit
  --recurse, --no-recurse, -r
                        recurse into subdirectories (default: False)
  --dry_run, --no-dry_run, -d
                        do not remove files (default: False)
  --verbose, --no-verbose, -v
                        Logs additional information while running. (default: False)
```
