import argparse
import os
import sys
from PIL import Image, ImageSequence

RESYTHON_VERSION = "0.1.0"

image_format = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "webp": "WEBP",
    "gif": "GIF",
    "png": "PNG"
}

def write_gif(frames, size):
    for frame in frames:
        result = frame.copy()
        result.thumbnail(size, resample=Image.Resampling.LANCZOS)
        yield result

def resize_image(image_files, arguments):
    output_name = arguments.name
    output_size = arguments.size
    ls = os.listdir()

    for img in image_files:
        file_extension = os.path.splitext(img)[-1][1:].lower()

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
                    if arguments.percent > 0:
                        width_px, height_px = im.size
                        output_size = (int(width_px * arguments.percent), int(height_px * arguments.percent))

                    if file_extension == 'gif':
                        frames = ImageSequence.Iterator(im)
                        frames = write_gif(frames, output_size)
                        om = next(frames)
                        om.info = im.info
                        om.save(outfile, save_all=True, append_images=list(frames))
                    else:
                        if arguments.t:
                            im.thumbnail(output_size, resample=Image.Resampling.LANCZOS)
                            im.save(outfile, image_format[file_extension])
                        else:
                            resized = im.resize(output_size, resample=Image.Resampling.LANCZOS)
                            resized.save(outfile)

            except Exception as err:
                print(err)
                print("Failed to create thumbnail")
        else:
            print("Output file exists Chief")


# ===== specify arguments
parser = argparse.ArgumentParser(prog="resython", description="Command line utility to resize multiple images")

output_display = parser.add_mutually_exclusive_group()
output_display.add_argument("-q", "--quite", help="decrease output verbosity", action="store_true")
output_display.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
output_display.add_argument("--version", help="display the program's current version", action="store_true")

mode_group = parser.add_mutually_exclusive_group()
mode_group.add_argument("-t", help="set to thumbnail mode, aspect ratio reserved, for gif image currently only thumbnail mode supported, still experimental", action="store_true")
mode_group.add_argument("-r", help="set to resize mode, aspect ratio not reserved", action="store_true", default=True)

size_format_group = parser.add_mutually_exclusive_group()
size_format_group.add_argument("-p", "--percent", help="specify the output size by percentage (0.0 - 1.0)", type=float, default=-1)
size_format_group.add_argument("-s", "--size", help="specify the output size (default 400 240)", nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'), default=(400, 240))

parser.add_argument("FILE", help="image to resize", nargs="*")
parser.add_argument("-n", "--name", help="specify the output name, will not change the extension")

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
