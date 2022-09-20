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

### Supported image format
- JPG/JPEG
- GIF
- WEBP
- PNG

### How to use

**Resize Single Image**

using default property
```bash
resipy img1.jpg  # img1.resized.jpg
```
default output name is `filename.resized.extension`, if `-t` flag used output file extension will be `thumbnail` so `img1.jpg -> img1.thumbnail`

specify the output name (will not change the extension)
```bash
resipy img1.jpg -n "output1"  # output1.jpg
```
change the output size to `300px` width and `200px` height
```bash
resipy img1.jpg -n "output1" -s 300 200
```
resize to half its size
```bash
resipy img1.jpg -n "output1" -p 0.5
```
create a thumbnail
```bash
resipy img1.jpg -t -s 200 200  # img1.thumbnail
```  

**Resize Multiple Images**  

using default property
```bash
resipy img1.jpg img2.jpg img3.png
```
output 
```
img1.jpg -> img1.resized.jpg
img2.jpg -> img2.resized.jpg
img3.png -> img3.resized.png
```
specify output name
```bash
resipy cat.jpg dog.jpg duck.png -n "output"
```

output 
```
cat.jpg -> output1.jpg
dog.jpg -> output2.jpg
duck.png -> output3.png
```
specify output size
```bash
resipy cat.jpg dog.jpg duck.png -n "output" -s 400 240
```
using percentage
```bash
resipy cat.jpg dog.jpg duck.png -n "output" -p 0.75
```
create thumbnail
```bash
resipy cat.jpg dog.jpg duck.png -n "output" -t
```
specify output size for each file
```bash
resipy cat.jpg dog.jpg duck.png -n "mycat" "mydog" "myduck"
```
output
```
cat.jpg -> mycat.jpg
dog.jpg -> mydog.jpg
duck.png -> myduck.png
```

### TODO
- more image support
- proper verbose message
