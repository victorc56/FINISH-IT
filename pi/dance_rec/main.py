import random
import pyttsx3
import time
import cv2
import numpy as np
import tensorflow as tf
from picamera.array import PiRGBArray
from picamera import PiCamera

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Load your trained model
# Ensure the model expects input shape as (frames, height, width, channels)
# Example: model = tf.keras.models.load_model('path_to_your_model.h5')
model = tf.keras.models.load_model('my_video_model.h5')

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def play_sound(result):
    # This is a placeholder for playing sound. You'll need to integrate
    # an actual library for playing sound or use a simple solution based on the result
    if result == "win":
        text_to_speech("Congratulations, you won!")
    else:
        text_to_speech("Sorry, you lost.")

def predict_move(frames):
    # Assuming 'frames' is a list of frames already preprocessed
    # Convert to numpy array and add batch dimension
    frames_np = np.array(frames)[np.newaxis, ...]
    prediction = model.predict(frames_np)
    
    # Interpret your model's prediction here and return "win" or "loss"
    # This is a placeholder logic
    predicted_class = np.argmax(prediction, axis=1)
    if predicted_class == expected_class:
        return "win"
    else:
        return "loss"

def capture_frames():
    with PiCamera() as camera:
        camera.resolution = (224, 224)  # Match model input
        rawCapture = PiRGBArray(camera, size=(224, 224))
        frames = []
        start_time = time.time()

        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            frames.append(image)
            rawCapture.truncate(0)

            # Break after 5 seconds of capture
            if time.time() - start_time > 5:
                break
            
            # Poll every 20 frames (adjust based on your needs)
            if len(frames) >= 20:
                # Preprocess and predict here (you may select a subset of frames)
                result = predict_move(frames[-20:])  # Example: using the last 20 frames
                play_sound(result)
                break  # Exit after prediction, or adjust logic as needed

def main():
    while True:
        # Generate a random number to determine the expected dance move
        expected_class = random.randint(0, 2)  # Assuming classes are 0-indexed
        class_map = {0: "griddy", 1: "naenae", 2: "whip"}
        
        print(f"Please perform the dance move: {class_map[expected_class]}")
        time.sleep(2)  # Give the user time to get ready
        print("Start dancing now!")
        capture_frames()
        
        # Add logic to continue or break based on user input or condition
        break  # Placeholder to break the loop, adjust as needed

if __name__ == "__main__":
    main()
