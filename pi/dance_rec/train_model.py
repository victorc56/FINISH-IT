import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np
import cv2  # For image capture and preprocessing


train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    'training_data_pi/',
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(224, 224),
    batch_size=32)

validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    'training_data_pi/',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(224, 224),
    batch_size=32)

AUTOTUNE = tf.data.experimental.AUTOTUNE

train_dataset = train_dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.cache().prefetch(buffer_size=AUTOTUNE)

classes = ['griddy', 'naenae', 'whip']

interpreter = tf.lite.Interpreter(model_path="squeezenet_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Example model (modify according to your needs)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(len(classes), activation='softmax')  # 'classes' should be the list of your classes
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model (X_train, y_train should be your preprocessed dataset and labels)
model.fit(train_dataset, validation_data=validation_dataset, epochs=10)

# After training, evaluate your model and then convert it to TensorFlow Lite format for deployment
model.save('my_model.h5')  # Save your model

# Convert the model to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
