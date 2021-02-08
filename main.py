from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter.font as TkFont
from PIL import ImageTk,Image


image_paths = []
image_filenames = []

    image_paths.append(filename)

    label.configure(text=filename)

def print_images():
    for i in image_paths:
        image_filenames.append(ImageTk.PhotoImage(Image.open(i).resize((100,100), Image.ANTIALIAS)))
    for i in image_filenames:
        cv = Canvas(window)
        cv.pack(side="left")
        cv.create_image(0, 0, image=i, anchor='nw')






window = Tk()
window.config(background="white")


window.title("Breast Cancer Detection")
window.geometry('600x600')

flag=False

btn_image_1 = create_button(window, "Browse", lambda: get_image_path(label_image_1))
label_image_1=Label(window)
btn_image_1.pack()
label_image_1.pack()

btn_image_2 = create_button(window, "Browse", lambda: get_image_path(label_image_2))
label_image_2=Label(window)
btn_image_2.pack()
label_image_2.pack()

btn_image_3 = create_button(window, "Browse", lambda: get_image_path(label_image_3))
label_image_3=Label(window)
btn_image_3.pack()
label_image_3.pack()

btn_image_4 = create_button(window, "Browse", lambda: get_image_path(label_image_4))
label_image_4=Label(window)
btn_image_4.pack()
label_image_4.pack()

display_btn = create_button(window, "Print images", print_images)
display_btn.pack()

window.mainloop()
