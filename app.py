import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

cataract_model = "./models/Catract_Hybrid/Catract_Hybrid_keras_model.h5"
cataract_label = "./models/Catract_Hybrid/labels.txt"

dr_model = "./models/Diabetic_retinopathy/Diabetic_retinopathy_keras_model.h5"
dr_label = "./models/Diabetic_retinopathy/labels.txt"

glaucoma_model = "./models/Glaucoma/Glaucoma_keras_model.h5"
glaucoma_label = "./models/Glaucoma/labels.txt"

def get_normalized_image_array(image):
    data_array = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data_array[0] = normalized_image_array

    return data_array

def predict_presence_of_disease(disease, image):
    np.set_printoptions(suppress=True)

    if disease == "Cataract":
        model_path = cataract_model
        label_path = cataract_label
    elif disease == "Diabetic Retinopathy":
        model_path = dr_model
        label_path = dr_label
    elif disease == "Glaucoma":
        model_path = glaucoma_model
        label_path = glaucoma_label

    model = load_model(model_path, compile=False)
    class_names = open(label_path, "r").readlines()
    data_array = get_normalized_image_array(image)
    
    prediction = model.predict(data_array)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name, confidence_score

if __name__ == '__main__':

    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.image('./images/collabll-logo.png')

    html_temp = """
    
    <div style="background-color:#bcd2e8;padding:10px;margin-bottom: 30px;">
        <h2 style="color:#1e3f66;text-align:center;">Eye Disease Prediction</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    with st.form(key='columns_in_form'):

        col1, col2 = st.columns(2)
        image = Image.new('RGB', (224, 224))

        with col1:
            uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp"])

        with col2:
            selected_disease = st.selectbox('Eye Disease', ['Cataract', 'Diabetic Retinopathy', 'Glaucoma'])
            predict = st.form_submit_button(label='Get Prediction')

        if predict:
            if selected_disease is None:
                prediction = "Disease is not selected!"
            elif image is None:
                prediction = "Image is not uploaded!"
            else:
                class_name, confidence_score = predict_presence_of_disease(selected_disease, image)
                prediction = f"{' '.join(class_name.strip().split()[1:])} (Confidence Score: {round(confidence_score, 8)}%)"

            st.text_area("Result", prediction)
            
            if uploaded_image is not None:
                image = Image.open(uploaded_image).convert("RGB")
                st.image(image, caption='Uploaded Image', use_column_width=True)
