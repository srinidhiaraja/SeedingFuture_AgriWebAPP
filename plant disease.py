import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
import cv2

plant_models = {
    'Rice': ('ricemodel.h5', ['Bacterial leaf blight', 'Brown spot', 'Leaf smut'], (180, 180)),
    'Pepper': ('peppermodel.h5', ['pepper_bell_bacterial_spot', 'pepper_healthy'], (256, 256)),
    'Cotton': ('cottonmodel2.h5', ['diseased cotton leaf', 'diseased cotton plant', 'fresh cotton leaf','fresh cotton plant'], (180, 180))
}
st.title('Plant Disease Detection')
st.subheader('Select Plant Type:')
selected_option = st.selectbox("Select Plant Type:", list(plant_models.keys()))

def read_file_as_image(data) -> np.array:
    image = np.array(data)
    return image

def resize_image(image, target_size):
    resized_image = cv2.resize(image, target_size)
    return resized_image

def perform_disease_detection(model_path, class_names, uploaded_image, target_size):
    model = tf.keras.models.load_model(model_path)
    resized_image = resize_image(uploaded_image, target_size)
    image_batch = np.expand_dims(resized_image, axis=0)
    predictions = model.predict(image_batch)
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return predicted_class, confidence
if selected_option != 'Select Plant Type':
    model_path, class_names, target_size = plant_models[selected_option]
    uploaded_file = st.file_uploader(f"Upload {selected_option} Image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file)
        st.image(uploaded_image, caption=f"Uploaded {selected_option} Image", width=250)
        uploaded_image = read_file_as_image(uploaded_image)
        predicted_class, confidence = perform_disease_detection(model_path, class_names, uploaded_image, target_size)
        st.write("Predicted Class:", predicted_class)
        #st.write("Confidence Level:", confidence)
else:
    st.write("Please select a plant type.")
