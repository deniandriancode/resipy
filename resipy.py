########## IMPORTS ###########
import argparse
import os
import sys
from PIL import Image, ImageSequence, ImageTk
import viewer

###### GLOBAL VARIABELS ######
PROG_NAME = "resipy"
RESIPY_VERSION = "0.4.0"

image_format = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "webp": "WEBP",
        "gif": "GIF",
        "png": "PNG",
        "ico": "ICO",
        "bmp": "BMP"
}

######################### NOTES ###########################
#
# if user uses -t flag, the extension will be '.thumbnail'
# else the extension will be the same as the input
# 
# if function does not return value, then return 0 to
# indicate that it run successfully
#
# TODO : add image support
# TODO : copy image to multiple names
# TODO : image->gray
# TODO : image viewer zoom (gif support)
# TODO : proper verbose image
#
###########################################################

def normal_message(input_name, output_name):
        """Display default message to user"""
        print("resizing : %s -> %s" % (input_name, output_name))
        return 0


def verbose_message(input_name, output_name):
        """Display more verbose message to user"""
        print("================================")
        print(" resizing : %s ===> %s" % (input_name, output_name))
        print("================================")
        print()
        return 0


def write_gif(outfile, size, args, input_file):
        """GIF image resizer"""
        is_thumbnail = args.t
        im = Image.open(input_file)
        frames = ImageSequence.Iterator(im)
        file_extension = os.path.splitext(input_file)[1][1:].lower()

        arr = []
        if is_thumbnail:
                for frame in frames:
                        tmp = frame.copy()
                        tmp.thumbnail(size, resample=Image.Resampling.LANCZOS)
                        arr.append(tmp)
        else:
                for frame in frames:
                        tmp = frame.copy()
                        resized = tmp.resize(size)
                        arr.append(resized)

        om = arr[0]  # copy the first frame
        om.info = im.info
        if args.verbose:
                verbose_message(input_file, outfile)
        elif args.quite:
                pass
        else:
                normal_message(input_file, outfile)

        if is_thumbnail:
                om.save(outfile, format=image_format[file_extension], save_all=True, append_images=arr)
        else:
                om.save(outfile, save_all=True, append_images=arr)

        return 0

def write_image(filename, im, output_options, args):
        """Static image resizer"""
        outfile = output_options['outfile']
        outsize = output_options['size']
        file_extension = output_options['extension']
        if args.t:
                if args.verbose:
                        verbose_message(filename, outfile)
                elif args.quite:
                        pass
                else:
                        normal_message(filename, outfile)

                im.thumbnail(outsize, resample=Image.Resampling.LANCZOS)
                im.save(outfile, image_format[file_extension])
        else:
                if args.verbose:
                        verbose_message(filename, outfile)
                elif args.quite:
                        pass
                else:
                        normal_message(filename, outfile)

                resized = im.resize(outsize, resample=Image.Resampling.LANCZOS)
                resized.save(outfile)

        return 0

def get_output_name(filename, output_name, args):
        if args.name: # if user provide output name, do the following
                outfile = output_name + os.path.splitext(filename)[-1]
                if args.t:
                        outfile = output_name + ".thumbnail"
        else: # else use the default name
                outfile = os.path.splitext(filename)[0] + ".resized" + os.path.splitext(filename)[-1]
                if args.t:
                        outfile = os.path.splitext(filename)[0] + ".thumbnail"

        return outfile


def write_base(filename, outfile, file_extension, args):
        try:
                with Image.open(filename) as im:
                        if args.percent > 0: # if value of percent is positive/valid value, do the following
                                width_px, height_px = im.size
                                output_size = (int(width_px * args.percent), int(height_px * args.percent))
                        else:
                                print(f"Value `percent` cannot be less than or equals to zero\nTry `{PROG_NAME} --help` for more information")

                        if file_extension == 'gif':
                                write_gif(outfile, output_size, args, filename)
                        else:
                                output_options = {
                                                "outfile": outfile,
                                                "size": output_size,
                                                "extension": file_extension
                                                }
                                write_image(filename, im, output_options, args)

        except Exception as err:
                print(err)
                print("Failed to resize image")

        return 0


def resize_image(image_files, arguments):
        """Resize logic function"""
        output_size = arguments.size
        output_filename = arguments.name
        file_length = len(image_files)
        name_length = len(output_filename) if output_filename else 0
        ls = os.listdir()

        if name_length == file_length:
                for img, outname_fin in zip(image_files, output_filename): # iterate through filename arguments
                        file_extension = os.path.splitext(img)[-1][1:].lower()

                        outfile = get_output_name(img, outname_fin, arguments)

                        if not arguments.force:  # if user did not use `-f` or `--force` flag, do the following
                                if outfile not in ls:  # if output file doesn't exists, do the following
                                        write_base(img, outfile, file_extension, arguments)
                                else: # else (the output name is already exists) exit the program
                                        print(f"Output file with name '{outfile}' exists. To override or replace the existing file add `-f` flag")
                                        sys.exit()
                        else: # else override the existing file
                                print(f"replacing '{outfile}'")
                                write_base(img, outfile, file_extension, arguments)
        elif name_length == 1:
                suffix_counter = 0
                for img in image_files: # iterate through filename arguments
                        file_extension = os.path.splitext(img)[-1][1:].lower()
                        output_fin = output_filename[0] + str(suffix_counter + 1)

                        outfile = get_output_name(img, output_fin, arguments)

                        if not arguments.force:  # if user did not use `-f` or `--force` flag, do the following
                                if outfile not in ls:  # if output file doesn't exists, do the following
                                        write_base(img, outfile, file_extension, arguments)
                                else: # else (the output name is already exists) exit the program
                                        print(f"Output file with name '{outfile}' exists. To override or replace the existing file add `-f` flag")
                                        sys.exit()
                        else: # else override the existing file
                                if outfile in os.listdir():
                                        print(f"replacing '{outfile}'")
                                write_base(img, outfile, file_extension, arguments)
                        
                        suffix_counter += 1
        elif name_length == 0:
                for img in image_files: # iterate through filename arguments
                        file_extension = os.path.splitext(img)[-1][1:].lower()
                        output_fin = os.path.splitext(img)[0]

                        outfile = get_output_name(img, output_fin, arguments)

                        if not arguments.force:  # if user did not use `-f` or `--force` flag, do the following
                                if outfile not in ls:  # if output file doesn't exists, do the following
                                        write_base(img, outfile, file_extension, arguments)
                                else: # else (the output name is already exists) exit the program
                                        print(f"Output file with name '{outfile}' exists. To override or replace the existing file add `-f` flag")
                                        sys.exit()
                        else: # else override the existing file
                                print(f"replacing '{outfile}'")
                                write_base(img, outfile, file_extension, arguments)
        else:
                print("Number of file argument and output name didn't match. Failed to resize image")
                sys.exit()

        return 0


def parse_args():
        """Initialize argument parser"""
        parser = argparse.ArgumentParser(prog=f"{PROG_NAME}", description="Command line utility to resize multiple images")

        output_display = parser.add_mutually_exclusive_group()
        output_display.add_argument("-q", "--quite", help="decrease output verbosity", action="store_true", default=False)
        output_display.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)
        output_display.add_argument("-V", "--version", help="display the program's current version", action="store_true")

        mode_group = parser.add_mutually_exclusive_group()
        mode_group.add_argument("-t", help="set to thumbnail mode, aspect ratio reserved", action="store_true")
        mode_group.add_argument("-r", help="set to resize mode, aspect ratio not reserved", action="store_true", default=True)

        size_format_group = parser.add_mutually_exclusive_group()
        size_format_group.add_argument("-p", "--percent", help="specify the output size by percentage (0.0 - 1.0)", type=float, default=0.5)
        size_format_group.add_argument("-s", "--size", help="specify the output size in pixel, if used with `-t`flag, it will take the smallest value (default 400 240)", nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'), default=(400, 240))

        parser.add_argument("FILE", help="image to resized", nargs="*")
        parser.add_argument("-n", "--name", help="specify the output name, will not change the extension", nargs="*")
        parser.add_argument("-f", "--force", help="override/replace the output file if exists", action="store_true", default=False)
        parser.add_argument("-vw", "--view", help="open/view an image", action="store_true", default=False)

        args = parser.parse_args()
        image_files = args.FILE
        return (args, image_files)


def main():
        """Driver function"""
        args, image_files = parse_args()

        if args.version:
                print(f"{PROG_NAME} {RESIPY_VERSION}")
                sys.exit()

        if args.view:
                viewer.view(image_files[0])
        elif args.FILE:
                resize_image(image_files, args)
        else:
                print(f"{PROG_NAME}: missing file arguments\nTry `{PROG_NAME} --help` for more information")

        return 0


if __name__ == '__main__':
        main()

