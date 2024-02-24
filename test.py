import random
import pyttsx3
import time
import picamera
import subprocess



def take_picture():
    imagecount=0;
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.capture('image'+str(imagecount)+'.jpg')
    imagecount=imagecount+1
    

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

def text_to_speech():
    print("yo")

def main():
    
    win=1
    

    while win:
        #random_number = random.randint(1,2,3)
        random_number=2
        if random_number == 1:
            text_to_speech()
        elif random_number == 2:
            take_picture()
        elif random_number == 3:
            take_video()
        else:
            print("Invalid random number generated.")
        
        #clean directory by removing pictures and videos
        command1="rm *.jpg"
        command2="rm *.mp4"
        subprocess.call(command1, shell=True)
        subprocess.call(command2, shell=True)


if __name__ == "__main__":
    main()
