import streamlit as st 
import numpy as np
from deepface import DeepFace
from PIL import Image

st.title("Human Emotion Detection")
st.write("Upload Image")

def analyize_image(img):
    result = DeepFace.analyze(img,actions=["emotion"])
    return result[0]["dominant_emotion"]

upload = st.file_uploader("choose an image",type=["png","jpg","jpeg"])
if upload is not None:
    img = Image.open(upload)
    img_np=np.array(img)
    st.image(img_np,caption="Upload image",use_column_width = True)
    emotions = analyize_image(img_np)
    st.write("Results",emotions)
