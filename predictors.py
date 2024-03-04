from keras.models import load_model
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

cataract_model = "./models/Catract_Hybrid/Catract_Hybrid_keras_model.h5"
cataract_label = "./models/Catract_Hybrid/labels.txt"

dr_model = "./models/Diabetic_retinopathy/Diabetic_retinopathy_keras_model.h5"
dr_label = "./models/Diabetic_retinopathy/labels.txt"

glaucoma_model = "./models/Glaucoma/Glaucoma_keras_model.h5"
glaucoma_label = "./models/Glaucoma/labels.txt"

def get_normalized_image_array(input_image_path):
    data_array = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(input_image_path).convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data_array[0] = normalized_image_array

    return data_array

def predict_presence_of_disease(disease, input_image_path):
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
    data_array = get_normalized_image_array(input_image_path)
    
    prediction = model.predict(data_array)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name, confidence_score