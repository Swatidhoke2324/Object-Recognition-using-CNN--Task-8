# Header Files & import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import easyocr
import socket

def carplate_detect(img):
    carplate_overlay = img.copy() 
    carplate_rects = car_plate_cls.detectMultiScale(carplate_overlay,scaleFactor=1.1, minNeighbors=3)
    for x,y,w,h in carplate_rects: 
        cv2.rectangle(carplate_overlay, (x,y), (x+w,y+h), (0,255,0), 20)     
    return carplate_overlay

# Create function to retrieve only the car plate region
def carplate_extract(image):
    carplate_rects = car_plate_cls.detectMultiScale(image,scaleFactor=1.1, minNeighbors=5)
    for x,y,w,h in carplate_rects: 
            carplate_img = image[y+15:y+h-10 ,x+15:x+w-20] # Adjusted to extract specific region of interest i.e. car license plate     
    return carplate_img

# Enlarge image for further processing later on
def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized_image

car_plate_cls = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

def model(filename):
    print("--------------------------------------------------------------------------\n")
    print("Reading image....")
    img = cv2.imread(filename)
    print("success\n")
    print("Converting it to gray....")
    img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("success\n")
    
    # Detect Plate
    print("Calling carplate_detect(img) function to detect number plate....")
    detected_carplate_img = carplate_detect(img)
    print("success\n")

    # Extract car license plate image
    print("Calling carplate_extract() function to retrieve only the car plate region....")
    carplate_extract_img = carplate_extract(img)
    print("success\n")
    print("Calling enlarge_img() function to enlarge the image....")
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    print("success\n")

    #Using Pre-Created Model
    print("Reading text from the enlarged number plate image....")
    reader = easyocr.Reader(['en'])
    result = reader.readtext(carplate_extract_img)
    final_result = result[1][1]+result[0][1]
    n=""
    f = final_result.split('-')
    f = n.join(f)
    f = f.replace(" ","")
    print("success\n")
    print("Detected number plate:")
    print(f)
    print("Returning detected no. plate.... ")
    print("--------------------------------------------------------------------------\n")
    return f
  







