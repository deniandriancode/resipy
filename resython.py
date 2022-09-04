import argparse
import os
import sys
from PIL import Image

RESYTHON_VERSION = "1.0.0"

image_format = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "webp": "WEBP",
    "gif": "GIF",
    "png": "PNG"
}

def resize_image(image_files, arguments):
    output_name = arguments.name
    ls = os.listdir()

    for img in image_files:
        file_extension = os.path.splitext(img)[-1][1:]

        if output_name:
            outfile = output_name + os.path.splitext(img)[-1]
            if arguments.t:
                outfile = output_name + ".thumbnail"
        else:
            outfile = os.path.splitext(img)[0] + ".resized" + os.path.splitext(img)[-1]
            if arguments.t:
                outfile = os.path.splitext(img)[0] + ".thumbnail"

        if outfile not in ls:  # if output file doesn't exists, do the following
            try:
                with Image.open(img) as im:
                    if arguments.t:
                        im.thumbnail(arguments.size)
                        im.save(outfile, image_format[file_extension])
                    else:
                        resized = im.resize(arguments.size)
                        resized.save(outfile)
            except Exception as err:
                print(err)
                print("Failed to create thumbnail")
        else:
            print("Output file exists Chief")

parser = argparse.ArgumentParser(prog="resython", description="Command line utility to resize multiple images")

output_display = parser.add_mutually_exclusive_group()
output_display.add_argument("-q", "--quite", help="decrease output verbosity", action="store_true")
output_display.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
output_display.add_argument("--version", help="display the program's current version", action="store_true")

mode_group = parser.add_mutually_exclusive_group()
mode_group.add_argument("-t", help="set to thumbnail mode, aspect ratio reserved", action="store_true")
mode_group.add_argument("-r", help="set to resize mode, aspect ratio not reserved", action="store_true", default=True)

parser.add_argument("FILE", help="image to resize", nargs="*")
parser.add_argument("-s", "--size", help="define the output size (default 400 240)", nargs=2, type=int, metavar=('width', 'height'), default=(400, 240))
parser.add_argument("-n", "--name", help="specify the output name")

args = parser.parse_args()
image_files = args.FILE


if __name__ == '__main__':
    if args.name and len(args.FILE) > 1:
        print("Cannot specify output name for multiple images")
        sys.exit()

    if args.version:
        print(f"resython {RESYTHON_VERSION}")
        sys.exit()

    if args.FILE:
        resize_image(image_files, args)
    else:
        print("resython: missing file arguments\nTry `resython --help` for more information")
