from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog


def create_button(window, text, command):
    button = Button(window, text=text, command=command)
    return button

def get_image_path(label):
    filename = filedialog.askopenfilename()
    label.configure(text=filename)

window = Tk()
window.config(background="white")


window.title("Breast Cancer Detection")
window.geometry('600x600')



label_image_1=Label(window, text="okay")
btn_image_1 = create_button(window, "Browse", lambda: get_image_path(label_image_1))
label_image_1.grid(column = 3, row = 1)
btn_image_1.grid(column = 3,row = 3)

label_image_2=Label(window, text="okay")
btn_image_2 = create_button(window, "Browse", lambda: get_image_path(label_image_2))
label_image_2.grid(column = 3, row = 4)
btn_image_2.grid(column = 3,row = 6)

label_image_3=Label(window, text="okay")
btn_image_3 = create_button(window, "Browse", lambda: get_image_path(label_image_3))
label_image_3.grid(column = 3, row = 8)
btn_image_3.grid(column = 3,row = 10)

label_image_4=Label(window, text="okay")
btn_image_4 = create_button(window, "Browse", lambda: get_image_path(label_image_4))
label_image_4.grid(column = 3, row = 12)
btn_image_4.grid(column = 3,row = 14)




window.mainloop()
