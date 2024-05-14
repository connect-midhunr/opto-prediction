import streamlit as st
from streamlit_modal import Modal
from keras.models import load_model
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os
import tensorflow as tf
import time
import math

from components import css, progress_bars_template

# Get the absolute path of the current working directory
current_directory = os.getcwd()

combined_model = os.path.join(current_directory, "models", "Combined Model", "keras_model.h5")
combined_label = os.path.join(current_directory, "models", "Combined Model", "labels.txt")

def is_blank_image(image):
    if image.mode != 'RGB':
        raise ValueError("Function is designed for RGB images only.")
    return all(x == 0 for x in image.convert('L').getextrema())

def get_normalized_image_array(image):
    data_array = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data_array[0] = normalized_image_array

    return data_array

def convert_prediction_result_to_dictionary(result):
    max_value = max(result)
    # Create a new array where only the maximum value remains unchanged, and others are set to 0
    result_array = [round(value * 100) if value == max_value else 0 for value in result]
    return {
        "GLAUCOMA_PROBABILITY": result_array[0],
        "CATARACT_PROBABILITY": result_array[1],
        "DR_PROBABILITY": result_array[2],
        "HR_PROBABILITY": result_array[4],
        "BRVO_PROBABILITY": result_array[3],
        "CRVO_PROBABILITY": result_array[5],
        "RAO_PROBABILITY": result_array[6],
    }

def predict_presence_of_disease(image):
    np.set_printoptions(suppress=True)

    model_path = combined_model
    model = load_model(model_path, compile=False)
    data_array = get_normalized_image_array(image)
    
    return convert_prediction_result_to_dictionary(model.predict(data_array)[0])

if __name__ == '__main__':

    image_error_message = Modal("Image is not uploaded!", key="demo-modal", padding=20, max_width=744)
    if image_error_message.is_open():
        with image_error_message.container():
            st.write("Please upload an image before clicking the 'Get Prediction' button.")

    st.write(css, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.image('./images/collabll-logo.png')

    html_temp = """
    <div style="background-color:#262730;padding:10px;margin-bottom: 30px;">
        <h2 style="color:#fff;text-align:center;">Eye Disease Prediction</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    with st.form(key='columns_in_form'):
        col1, col2 = st.columns(2)
        image = Image.new('RGB', (224, 224))

        with col1:
            uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp"])
            
            if uploaded_image:
                image = Image.open(uploaded_image).convert("RGB")
                st.image(image, caption='Uploaded Image', use_column_width=True)
            
            predict = st.form_submit_button(label='Get Prediction')

        with col2:
            if predict:
                print("Image:", image)
                if is_blank_image(image):
                    image_error_message.open()
                    print("Image is not uploaded!")
                else:
                    with st.spinner("Model Loading..."):
                        start_time = time.time()
                        predictions = predict_presence_of_disease(image)
                        end_time = time.time()
                        time_taken_in_seconds = end_time - start_time
                        
                        result_template = progress_bars_template.replace("{{GLAUCOMA_PROBABILITY}}", str(predictions["GLAUCOMA_PROBABILITY"]))
                        result_template = result_template.replace("{{CATARACT_PROBABILITY}}", str(predictions["CATARACT_PROBABILITY"]))
                        result_template = result_template.replace("{{DR_PROBABILITY}}", str(predictions["DR_PROBABILITY"]))
                        result_template = result_template.replace("{{HR_PROBABILITY}}", str(predictions["HR_PROBABILITY"]))
                        result_template = result_template.replace("{{BRVO_PROBABILITY}}", str(predictions["BRVO_PROBABILITY"]))
                        result_template = result_template.replace("{{CRVO_PROBABILITY}}", str(predictions["CRVO_PROBABILITY"]))
                        result_template = result_template.replace("{{RAO_PROBABILITY}}", str(predictions["RAO_PROBABILITY"]))
                        st.markdown(result_template, unsafe_allow_html=True)
                        
                        formatted_time_taken = f"Time taken: {int(time_taken_in_seconds // 60)} minutes and {round(time_taken_in_seconds % 60, 3)} seconds"
                        st.write(formatted_time_taken)
