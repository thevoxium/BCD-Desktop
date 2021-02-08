from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from email_sys import auto_email
import argparse
import torch
import utils
import models_torch as models
from functools import partial

list_of_image_paths = []

toaddr = "sdfds"



def create_button(window, text, command):
    button = Button(window, text=text, command=command)
    return button


def automail_btn(list_of_image_paths):
    print(b0, b1, b2)
    toaddr = email_entry.get()
    for list_of_image_path in list_of_image_paths:
        i = 0
        while i<len(list_of_image_path):
            if list_of_image_path[i]=='\\':
                list_of_image_path[i]='/'
            i=i+1

    auto_email(toaddr, list_of_image_paths, b0, b1, b2)

def get_email():
    toaddr = email_entry.get()
    print(toaddr)

#Sending
def get_image_path1():
    filename1 = filedialog.askopenfilename()
    datum_l_cc = utils.load_images(filename1)
    label_image.configure(text="Upload L-MLO")
    list_of_image_paths.append(filename1)
    return datum_l_cc

def get_image_path2():
    filename2 = filedialog.askopenfilename()
    datum_r_cc = utils.load_images(filename2)
    label_image.configure(text="Upload R-MLO")
    list_of_image_paths.append(filename2)
    return datum_r_cc

def get_image_path3():
    filename3 = filedialog.askopenfilename()
    datum_l_mlo = utils.load_images(filename3)
    label_image.configure(text="Upload R-CC")
    list_of_image_paths.append(filename3)
    return datum_l_mlo

def get_image_path4():
    filename4 = filedialog.askopenfilename()
    datum_r_mlo = utils.load_images(filename4)
    list_of_image_paths.append(filename4)
    label_image.configure(text="All 4 Uploaded")
    return datum_r_mlo



def inference(parameters, verbose=True):
    """
    Function that creates a model, loads the parameters, and makes a prediction
    :param parameters: dictionary of parameters
    :param verbose: Whether to print predicted probabilities
    :return: Predicted probabilities for each class
    """
    # resolve device
    device = torch.device(
        "cuda:{}".format(parameters["gpu_number"]) if parameters["device_type"] == "gpu"
        else "cpu"
    )

    # construct models
    model = models.BaselineBreastModel(device, nodropout_probability=1.0, gaussian_noise_std=0.0).to(device)
    model.load_state_dict(torch.load(parameters["model_path"]))

    # load input images and prepare data
    x = {
        "L-CC": torch.Tensor(get_image_path1()).permute(0, 3, 1, 2).to(device),
        "L-MLO": torch.Tensor(get_image_path3()).permute(0, 3, 1, 2).to(device),
        "R-CC": torch.Tensor(get_image_path2()).permute(0, 3, 1, 2).to(device),
        "R-MLO": torch.Tensor(get_image_path4()).permute(0, 3, 1, 2).to(device),
    }

    # run prediction
    with torch.no_grad():
        prediction_birads = model(x).cpu().numpy()

    if verbose:
        # nicely prints out the predictions
        birads0_prob = prediction_birads[0][0]
        birads1_prob = prediction_birads[0][1]
        birads2_prob = prediction_birads[0][2]
        global b0
        global b1
        global b2
        b0 = birads0_prob
        b1 = birads1_prob
        b2 = birads2_prob
        print(b0, b1, b2)
        label_image_5.configure(text="Predicted!")
        label1=Label(window, text="BI-RADS prediction: ")
        label2=Label(window, text='BI-RADS 0: ' + str(birads0_prob))
        label3=Label(window, text='BI-RADS 1: ' + str(birads1_prob))
        label4=Label(window, text= 'BI-RADS 2: ' + str(birads2_prob))
        label1.pack()
        label2.pack()
        label3.pack()
        label4.pack()


parser = argparse.ArgumentParser(description='Run Inference')
parser.add_argument('--model-path', default='saved_models/model.p')
parser.add_argument('--device-type', default="cpu")
parser.add_argument('--gpu-number', default=0, type=int)
args = parser.parse_args()

parameters_ = {
    "model_path": args.model_path,
    "device_type": args.device_type,
    "gpu_number": args.gpu_number,
    "input_size": (2600, 2000),
}





window = Tk()
window.config(background="white")


window.title("Breast Cancer Detection")
window.geometry('300x300')



label_image=Label(window, text="Upload L-CC")

label_image.pack()


label_image_5=Label(window, text="Predicting.....")
btn_image_5= create_button(window, "Run", lambda: inference(parameters_))
label_image_5.pack()
btn_image_5.pack()
"""
test_email = Text(window, height=1)
test_email.pack()

enter_email_btn = create_button(window, "Enter Email", get_email)
enter_email_btn.pack()
"""

email_entry = Entry(window)
email_entry.pack()
email_entry.bind("<Return>")


enter_email_btn = create_button(window, "Enter Email", get_email)
enter_email_btn.pack()
print(toaddr+"45454")

mail_btn = create_button(window, "Send Email", lambda: automail_btn(list_of_image_paths))
mail_btn.pack()

window.mainloop()
