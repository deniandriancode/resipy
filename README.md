# Resipy  

Command line utility to resize multiple images  

```
usage: resipy [-h] [-q | -v | -V] [-t | -r] [-p PERCENT | -s WIDTH HEIGHT]
              [-n [NAME ...]] [-f]
              [FILE ...]

Command line utility to resize multiple images

positional arguments:
  FILE                  image to resized

options:
  -h, --help            show this help message and exit
  -q, --quite           decrease output verbosity
  -v, --verbose         increase output verbosity
  -V, --version         display the program's current version
  -t                    set to thumbnail mode, aspect ratio reserved
  -r                    set to resize mode, aspect ratio not reserved
  -p PERCENT, --percent PERCENT
                        specify the output size by percentage (0.0 - 1.0)
  -s WIDTH HEIGHT, --size WIDTH HEIGHT
                        specify the output size in pixel, if used with
                        `-t`flag, it will take the smallest value (default 400
                        240)
  -n [NAME ...], --name [NAME ...]
                        specify the output name, will not change the extension
  -f, --force           override/replace the output file if exists
```
