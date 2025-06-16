import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load your trained tomato model
model = load_model("models/my_tomato_model.h5")

# Class labels based on 10 output nodes
class_labels = [
    "Bacterial_spot",
    "Early_blight",
    "Healthy",
    "Late_blight",
    "Leaf_Mold",
    "Septoria_leaf_spot",
    "Spider_mites",
    "Target_Spot",
    "YellowLeaf_Curl_Virus",
    "Mosaic_Virus"
]

# Load and preprocess test image
test_image_path = "static/uploads/test_tomato.jpg"  # Update if needed
img = image.load_img(test_image_path, target_size=(150, 150))  # Model expects 150x150
img_array = image.img_to_array(img).astype('float32') / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Debug shapes
print("✅ Preprocessed image shape:", img_array.shape)
print("📦 Model expects input shape:", model.input_shape)

# Run prediction
prediction = model.predict(img_array)

# Extract info
predicted_index = np.argmax(prediction)
predicted_label = class_labels[predicted_index]
confidence = round(float(np.max(prediction)) * 100, 2)

# Console outputs
print("🔍 Raw Prediction Probabilities:", prediction)
print("📏 Shape of prediction output:", prediction.shape)
print("✅ Sum of probabilities:", np.sum(prediction))
print("🔢 Predicted Class Index:", predicted_index)
print("🏷️ Predicted Class Label:", predicted_label)
print("📊 Confidence (%):", confidence)
