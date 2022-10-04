import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
import sys

IMAGE_DIMENSION = {"x": 0, "y": 0}

def resize_activate(event, prev_size, l_label, l_img_pil):
        win_size = prev_size.split("+")[0]
        win_width, win_height = win_size.split("x")
        print(f"width : {win_width}, height : {win_height}")

def zoom(event, root, label, image_pil, mode):
        global IMAGE_DIMENSION
        IMAGE_DIMENSION["x"] = int(IMAGE_DIMENSION["x"] + (mode * IMAGE_DIMENSION["x"] * 0.1))
        IMAGE_DIMENSION["y"] = int(IMAGE_DIMENSION["y"] + (mode * IMAGE_DIMENSION["y"] * 0.1))

        image_resized = image_pil.resize(size=(IMAGE_DIMENSION["x"], IMAGE_DIMENSION["y"]))
        image = ImageTk.PhotoImage(image_resized)

        label.image = image
        label.configure(image=image)

def update_gif(index, frames, frame_count, l_label, l_root):
        frame = frames[index]
        index += 1
        if index == frame_count:
                index = 0
        l_label.configure(image=frame)
        l_root.after(100, lambda: update_gif(index, frames, frame_count, l_label, l_root))

def view(filename):
        global IMAGE_DIMENSION
        main_bg = "#050505"

        root = tk.Tk()
        root.config(bg=main_bg)

        window_icon_src = os.path.join(os.path.abspath('.'), 'pyicon.png')
        window_icon = tk.PhotoImage(file=window_icon_src)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        extension = os.path.splitext(filename)[1][1:].lower()
        image_view_size = 750

        image_src = os.path.join(os.path.abspath("."), filename)
        image_pil = Image.open(image_src)

        max_img_size = max(image_pil.size)

        image_pil.thumbnail(size=(image_view_size, image_view_size))

        window_width, window_height = image_pil.size
        IMAGE_DIMENSION["x"], IMAGE_DIMENSION["y"] = image_pil.size
        image = ImageTk.PhotoImage(image_pil)
        label = tk.Label(root, image=image, anchor=tk.CENTER, bg=main_bg)
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        if extension == "gif":
                image_itr = ImageSequence.all_frames(image_pil)
                frame_count = len(image_itr)
                frames = [tk.PhotoImage(file=filename, format="gif -index {}".format(i)) for i in range(frame_count)]
        else:
                max_img_size = max(image_pil.size)

        # root.bind('<Configure>', lambda event: resize_activate(event, root.geometry(), label, image_pil))
        root.bind("<Control-KeyPress-minus>", lambda event: zoom(event, root, label, image_pil, -1))
        root.bind("<Control-Shift-KeyPress-plus>", lambda event: zoom(event, root, label, image_pil, 1))
        root.title(f"resipy v0.3.0: {os.path.join(os.path.abspath('.'), filename)}")
        root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        root.after(0, lambda: update_gif(0, frames, frame_count, label, root)) if extension == "gif" else 0
        root.iconphoto(True, window_icon)

        root.mainloop()




