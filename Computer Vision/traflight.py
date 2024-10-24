import streamlit as st 
import torch
import cv2
import numpy as np 
from PIL import Image

model=torch.hub.load("ultralytics/yolov5", "yolov5s") #step1 load model 
st.title("Traffic Light Detection")
def classify_color(image,box): #step 2 
    x1,y1,x2,y2=map(int,box)
    # print("hello",x1,y1,x2,y2)
    cropped_image=image[y1:y2,x1:x2]
    #convert image to hsv filter 
    hsv_image=cv2.cvtColor(cropped_image,cv2.COLOR_RGB2HSV)    
    
    #DEFINE COLORS IN HSV
    red_lower1 = np.array([0, 70, 50])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 70, 50])
    red_upper2 = np.array([180, 255, 255])
    green_lower = np.array([40, 40, 40])
    green_upper = np.array([80, 255, 255])
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    
    #check for red 
    red_mask1=cv2.inRange(hsv_image,red_lower1,red_upper1)
    red_mask2=cv2.inRange(hsv_image,red_lower2,red_upper2)
    
    red_mask=red_mask1 | red_mask2
    red_pixels=cv2.countNonZero(red_mask)
    
    #check for green
    green_mask=cv2.inRange(hsv_image,green_lower,green_upper)
    green_pixels=cv2.countNonZero(green_mask)
    
    #check for yellow
    yellow_mask=cv2.inRange(hsv_image,yellow_lower,yellow_upper)
    yellow_pixels=cv2.countNonZero(yellow_mask)
    
    
    if max(red_pixels,green_pixels,yellow_pixels) ==yellow_pixels:
        return "Yellow"
    elif max(red_pixels,green_pixels,yellow_pixels) ==green_pixels:
        return "Green"
    elif max(red_pixels,green_pixels,yellow_pixels) ==red_pixels:
        return "Red"
    else:
        return "UNKnOWN"
upload_file=st.file_uploader("Choose an image",type=["jpg","png","jpeg"])

if upload_file is not None:
    img=Image.open(upload_file)
    image_np=np.array(img)
    st.image(image_np,caption="uploaded image",use_column_width=True)
    image_resized=cv2.resize(image_np,(640,480))
    results=model(image_resized)
    
    box=results.xyxy[0].numpy()
    # print("Hello",box)
    for b in box:
        label=results.names[int(b[5])]
        if label=="traffic light":
            color=classify_color(image_resized,b[:4])
            st.write(f"Detected color is {color}")
            
    st.image(results.render()[0],caption="Detected Traffic-lights",use_column_width=True)