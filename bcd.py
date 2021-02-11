from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from email_sys import auto_email
import argparse
import torch
import utils
import models_torch as models
from functools import partial

#stores all the uploaded images as an array for mailing purposes
list_of_image_paths = []

#receiver address initialization
toaddr = "sdfds"

#Function to create button
def create_button(window, text, command):
    button = Button(window, text=text, command=command)
    return button

#Function to mail and links to email_sys.py
def automail_btn(list_of_image_paths):
    #print(b0, b1, b2)
    toaddr = email_entry.get()
    for list_of_image_path in list_of_image_paths:
        i = 0
        while i<len(list_of_image_path):
            if list_of_image_path[i]=='\\':
                list_of_image_path[i]='/'
                #\ converted to / for reading purposes,tkinter typical file address notation
            i=i+1

    auto_email(toaddr, list_of_image_paths, b0, b1, b2)

#Extracts the input from Entry widget/Input field 
def get_email():
    toaddr = email_entry.get()
    #print(toaddr)

#returns the file_address/file path
def openfilename():  
    # open file dialog box to select image 
    # The dialogue box has a title "Open" 
    filename = filedialog.askopenfilename(title ='Upload the Scanned Images') 
    return filename

#To remove seek and read attribute error with PIL
def write_file(address,fname):
    file = open(fname,"w+")
    file.write(address)
    file.close() 

#Sending 4 images to utilis for resizing and transforming and return to the inference.
#Links inference to utilis.
#Also places the images on the applicaton window.
#Also adds the images to the array for mailing.
def get_image_path1():
    filename1 = openfilename()
    #Image Positioning
    try: 
      x = filename1
      write_file(x,"upload");
      img =Image.open(x)
    except:
      x = 'error.png' #If canceled uploading
      img =Image.open(x)
    img = img.resize((100, 130), Image.ANTIALIAS) 
    img = ImageTk.PhotoImage(img) 
    panel = Label(window, image = img) 
    panel.image = img 
    panel.place(relx=0.2105263157894,y=75)

    datum_l_cc = utils.load_images(filename1)
    label_image.configure(text="Upload L-MLO")
    list_of_image_paths.append(filename1) #adds the image to the array for mailing
    return datum_l_cc

def get_image_path2():
    filename2 = openfilename() 
    #Image Positioning
    try: 
      x = filename2
      write_file(x,"upload");
      img =Image.open(x)
    except:
      x = 'error.png' #If canceled uploading
      img =Image.open(x)
    img = img.resize((100, 130), Image.ANTIALIAS) 
    img = ImageTk.PhotoImage(img) 
    panel = Label(window, image = img) 
    panel.image = img 
    panel.place(relx=0.5789473684210,y=75)
    
    datum_r_cc = utils.load_images(filename2) 
    label_image.configure(text="Upload R-MLO")
    list_of_image_paths.append(filename2) #adds the image to the array for mailing
    return datum_r_cc

def get_image_path3():
    filename3 = openfilename() 
    #Image Positioning
    try: 
      x = filename3
      write_file(x,"upload");
      img =Image.open(x)
    except:
      x = 'error.png' #If canceled uploading
      img =Image.open(x)
    img = img.resize((100, 130), Image.ANTIALIAS) 
    img = ImageTk.PhotoImage(img) 
    panel = Label(window, image = img) 
    panel.image = img 
    panel.place(relx=0.2105263157894,y=280)

    datum_l_mlo = utils.load_images(filename3)
    label_image.configure(text="Upload R-CC")
    list_of_image_paths.append(filename3) #adds the image to the array for mailing
    return datum_l_mlo

def get_image_path4():
    filename4 = openfilename()
    #Image Positioning 
    try: 
      x = filename4
      write_file(x,"upload");
      img =Image.open(x)
    except:
      x = 'error.png' #If canceled uploading
      img =Image.open(x)
    img = img.resize((100, 130), Image.ANTIALIAS) 
    img = ImageTk.PhotoImage(img) 
    panel = Label(window, image = img) 
    panel.image = img 
    panel.place(relx=0.5789473684210,y=280)

    datum_r_mlo = utils.load_images(filename4)
    list_of_image_paths.append(filename4)
    label_image.configure(text="All 4 Uploaded") #adds the image to the array for mailing
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
        #introducing  3 global variables so that they can be accesed from automail
        global b0
        global b1
        global b2
        b0 = birads0_prob
        b1 = birads1_prob
        b2 = birads2_prob
        #print(b0, b1, b2)
        label_image_1.configure(text="Predicted!")
        label1=Label(window, text="BI-RADS prediction: ",anchor="e", justify = CENTER)
        label2=Label(window, text='BI-RADS 0: ' + str(birads0_prob),anchor="e", justify = CENTER)
        label3=Label(window, text='BI-RADS 1: ' + str(birads1_prob),anchor="e", justify = CENTER)
        label4=Label(window, text= 'BI-RADS 2: ' + str(birads2_prob),anchor="e", justify = CENTER)
        label1.place(relx=0.47,y=500)
        label2.place(relx=0.47,y=520)
        label3.place(relx=0.47,y=540)
        label4.place(relx=0.47,y=560)

#Parser Args
parser = argparse.ArgumentParser(description='Run Inference')
parser.add_argument('--model-path', default='saved_models/model.p')
parser.add_argument('--device-type', default="cpu")
parser.add_argument('--gpu-number', default=0, type=int)
args = parser.parse_args()

#Parameters passed to inference
parameters_ = {
    "model_path": args.model_path,
    "device_type": args.device_type,
    "gpu_number": args.gpu_number,
    "input_size": (2600, 2000),
}

#------------------------------------------------------------------------------------------------------------------------------------
#Main starts from here
window = Tk()
window.config(background="white")

window.title("Breast Cancer Detection")
window.geometry('475x750')
 
window.resizable(width = True, height = True) 
  
label_image=Label(window, text="Upload L-CC")
label_image.place(relx=0.47,y=470)

label_image_1=Label(window, text="Predicting.....",anchor="e", justify = CENTER)
btn_image_1= create_button(window, "Run", lambda: inference(parameters_))
label_image_1.place(relx=0.47,y=495)
btn_image_1.place(relx=0.49,y=600)

email_entry = Entry(window,borderwidth=3, justify = CENTER,width=25)
email_entry.focus_force() 
email_entry.pack()
email_entry.insert(0, "Input Email-Id")
email_entry.bind("<Return>")

mail_btn = create_button(window, "Send Email", lambda: automail_btn(list_of_image_paths))
mail_btn.pack()

window.mainloop()
