from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

import argparse
import torch
import utils
import models_torch as models

def create_button(window, text, command):
    button = Button(window, text=text, command=command)
    return button

#Sending
def get_image_path1():
    filename1 = filedialog.askopenfilename()
    datum_l_cc = utils.load_images(filename1)
    label_image.configure(text="Upload L-MLO")
    return datum_l_cc

def get_image_path2():
    filename2 = filedialog.askopenfilename()
    datum_r_cc = utils.load_images(filename2)
    label_image.configure(text="Upload R-MLO")
    return datum_r_cc

def get_image_path3():
    filename3 = filedialog.askopenfilename()
    datum_l_mlo = utils.load_images(filename3)
    label_image.configure(text="Upload R-CC")
    return datum_l_mlo

def get_image_path4():
    filename4 = filedialog.askopenfilename()
    datum_r_mlo = utils.load_images(filename4)
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
        label_image_5.configure(text="Predicted!")
        label1=Label(window, text="BI-RADS prediction: ")
        label2=Label(window, text='BI-RADS 0: ' + str(birads0_prob))
        label3=Label(window, text='BI-RADS 1: ' + str(birads1_prob))
        label4=Label(window, text= 'BI-RADS 2: ' + str(birads2_prob))
        label1.grid(column=3, row=22)
        label2.grid(column=3, row=24)
        label3.grid(column=3, row=26)
        label4.grid(column=3, row=28)


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
window.geometry('600x600')



label_image=Label(window, text="Upload L-CC")

label_image.grid(column = 3, row = 8)


label_image_5=Label(window, text="Predicting.....")
btn_image_5= create_button(window, "Run", lambda: inference(parameters_))
label_image_5.grid(column = 3, row = 16)
btn_image_5.grid(column = 3,row = 20)

window.mainloop()