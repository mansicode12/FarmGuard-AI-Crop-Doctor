import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D

# Create models directory if not exists
os.makedirs("models", exist_ok=True)

# Create a simple dummy model
def create_dummy_model(num_classes=3):
    model = Sequential([
        Conv2D(16, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(32, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Create and save dummy models
crops = ['wheat', 'rice', 'maize']
for crop in crops:
    model = create_dummy_model()
    model.save(f"models/my_{crop}_model.h5")
    print(f"Saved dummy model for {crop}")
