import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
import sys

def update_gif(index, frames, frame_count, l_label, l_root):
        frame = frames[index]
        index += 1
        if index == frame_count:
                index = 0
        l_label.configure(image=frame)
        l_root.after(45, lambda: update_gif(index, frames, frame_count, l_label, l_root))

def view(filename):
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

        root.title(f"resipy v0.3.0: {os.path.join(os.path.abspath('.'), filename)}")
        root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        root.after(0, lambda: update_gif(0, frames, frame_count, label, root)) if extension == "gif" else 0
        root.iconphoto(True, window_icon)

        root.mainloop()

# def resize_activate(event):
        # label.place_forget()
        # image_pil.thumbnail(size=(event.width, event.width))
        # label = tk.Label(root, image=image, anchor=tk.CENTER, bg=main_bg)
        # label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


# root.bind('<Configure>', resize_activate)

