import cv2
import numpy as np
import os
from tkinter import *
import base64
# Reading image

from PIL import Image,ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile

from pathlib import Path
from typing import Union
import argparse

import cv2



def showimage():
    global img
    fln = filedialog.askopenfilename(initialdir=os.getcwd(),title="select image file",filetypes=(("JPG File",".jpg"),("PNG File",".png"),("JPEG File",".jpeg"),("All Files",".")))
    img=Image.open(fln)
    n=is_cartoon()
    round(n,2)
    print(n)
    if (n)>0.99:
        print("sorry!cannot accept it!")
    else:
        k=8
        gray = cv2.cvtColor(np.ascontiguousarray(img), cv2.COLOR_RGB2GRAY)


    # Peform adaptive threshold
        edges  = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 8)

    # cv2.imshow('edges', edges)

    # Defining input data for clustering
        data = np.float32(img).reshape((-1, 3))

    # Defining criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)

    # Applying cv2.kmeans function
        _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)


    # Reshape the output data to the size of input image
        result = center[label.flatten()]
        result = result.reshape((np.array(img)).shape)
    #cv2.imshow("result", result)
    # Convert the input image to gray scale


        gray = cv2.cvtColor(np.ascontiguousarray(img), cv2.COLOR_RGB2GRAY)

    # Perform adaptive threshold
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 8)
    #cv2.imshow('edges', edges)
    # Smooth the result
        blurred = cv2.medianBlur(result, 3)

    # Combine the result and edges to get final cartoon effect
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
        img = Image.fromarray(cartoon, 'RGB')
        img.thumbnail((350,400))
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img)
        lbl.image=img

def is_cartoon():
    # read and resize image
    img3 = cv2.resize(np.ascontiguousarray(img), (1024, 1024))

    # blur the image to "even out" the colors
    color_blurred = cv2.bilateralFilter(img3, 6, 250, 250)
    #cv2.imshow("blurred", color_blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # compare the colors from the original image to blurred one.
    diffs = []
    for k, color in enumerate(("b", "r", "g")):
        # print(f"Comparing histogram for color {color}")
        real_histogram = cv2.calcHist(img3, [k], None, [256], [0, 256])
        color_histogram = cv2.calcHist(color_blurred, [k], None, [256], [0, 256])
        diffs.append(
            cv2.compareHist(real_histogram, color_histogram, cv2.HISTCMP_CORREL)
        )

    r=sum(diffs) / 3
    print(r)
    return r

def savefile():
    filename = filedialog.asksaveasfile(mode='w',initialfile = 'Untitled.jpg', defaultextension=".jpg",filetypes=(("JPG File",".jpg"),("PNG File",".png"),("JPEG File",".jpeg"),("All Files",".")))
    img1 = ImageTk.getimage( img )
    im = img1.convert('RGB')
    im.save(filename)






root = Tk()


frm=Frame(root)
frm.pack(side=BOTTOM,padx=20,pady=20)

#define the position of the image


lbl=Label(root)
lbl.pack()
btn=Button(frm,text="cartoonify me!",command=showimage)
btn.pack(side=tk.LEFT)
btn2=Button(frm,text="Exit",command=root.destroy)
btn2.pack(side=tk.LEFT,padx=10)
button = Button(frm, text="save as", command=savefile)
button.pack(side=tk.RIGHT,padx=10)

text=Label(root, text="welcome to our project!!!")
text.pack(pady=50,padx=10)
text.config(font=('Helvetica bold',18))



root.title("image cartoonifier")
root.geometry("300x350")
root.mainloop()