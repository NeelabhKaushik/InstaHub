import tensorflow as tf
import numpy as np
from PIL import Image

# Load the Inception V3 model
model = tf.keras.applications.InceptionV3(include_top=True, weights='imagenet')

# Load and preprocess the image
img = Image.open("/Users/neelabhkaushik/Documents/CARS/new-ghost-white-fr-3-4-1-1598911711.jpg")
img = img.resize((299, 299))
x = tf.keras.preprocessing.image.img_to_array(img)
x = tf.keras.applications.inception_v3.preprocess_input(x)
x = np.expand_dims(x, axis=0)

# Predict the class of the image
preds = model.predict(x)
top_preds = tf.keras.applications.inception_v3.decode_predictions(preds, top=5)[0]

# Print the top predictions
for pred in top_preds:
    word = pred[1]
    new_wrd = word.replace("_", "")
    print(new_wrd)
    
    
    
def findd_class(self):

    np.set_printoptions(suppress=True)

    model = load_model("keras_Model.h5", compile=False)

    class_names = open("labels.txt", "r").readlines()

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(file_loc).convert("RGB")

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)
    