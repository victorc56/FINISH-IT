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
model = tf.keras.models.load_model('my_video_model.h5')

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def play_sound(result):
    if result:
        print("Congratulations, you got the dance move correct!")
    else:
        print("Sorry, that was not the correct dance move.")

def preprocess_frame(frame):
    # Resize frame to model's expected size
    frame_resized = cv2.resize(frame, (224, 224))
    # Normalize pixel values if your model expects normalization
    frame_normalized = frame_resized / 255.0
    return frame_normalized

def predict_move(frames):
    # Convert to numpy array, normalize, and add batch dimension
    frames_np = np.array(frames)
    prediction = model.predict(np.expand_dims(frames_np, axis=0))
    predicted_class = np.argmax(prediction, axis=1)[0]
    return predicted_class

def capture_frames(expected_class):
    with PiCamera() as camera:
        camera.resolution = (224, 224)
        camera.framerate = 24  # Adjust based on your needs
        rawCapture = PiRGBArray(camera, size=(224, 224))
        frames = []
        start_time = time.time()

        for _, frame in enumerate(camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)):
            if len(frames) >= 50:  # Capture 50 frames
                break
            image = frame.array
            frames.append(preprocess_frame(image))
            rawCapture.truncate(0)

    # Make prediction
    predicted_class = predict_move(frames)
    # Compare prediction with expected class
    result = predicted_class == expected_class
    play_sound(result)

def main():
    class_map = {0: "griddy", 1: "naenae", 2: "whip"}
    while True:
        expected_class = random.randint(0, 2)  # Generate a random dance move
        print(f"Please perform the dance move: {class_map[expected_class]}")
        time.sleep(5)  # Give the user time to get ready
        print("Start dancing now!")
        capture_frames(expected_class)

        # Placeholder for continuous running, modify as per your requirement
        user_input = input("Try again? (yes/no): ")
        if user_input.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
