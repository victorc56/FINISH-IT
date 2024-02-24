import random
import pyttsx3
import time
import picamera



def take_picture():
    imagecount=0;
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.capture('image'+str(imagecount)+'.jpg')
    imagecount=imagecount+1

def text_to_speech():
    engine = pyttsx3.init()
    text = "Hello, world! This is a text-to-speech test."
    engine.say(text)
    engine.runAndWait()
    print("Text-to-speech completed!")
    
    

def take_video():
    videocount=0;
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_recording('video' + str(videocount) + '.h264')
        print("Recording started...")
        camera.wait_recording(2)  # Record for 2 seconds
        camera.stop_recording()
        print("Recording stopped.")
    videocount=videocount+1


def main():
    win=true;
    

    while win:
        random_number = random.randint(1, 2)
        if random_number == 1:
            text_to_speech()
        elif random_number == 2:
            take_picture()
        elif random_number == 3:
            take_video()
        else:
            print("Invalid random number generated.")
    


if __name__ == "__main__":
    main()
