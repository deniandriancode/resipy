from PIL import Image
import os
import sys

filename = sys.argv[1]
im = Image.open(filename)
im.save("now.ico", size=[(128, 128)])
im.close()
