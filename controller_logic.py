import RPi.GPIO as GPIO
import time
import random

def main():

    score = 0

    valid = True
    Time = 30

    while valid:

        num = random.randint(0,2)

        if num == 0:
            if not game1(Time):
                print("Correct! +1")
                score = score + 1
            else:
                print("Wrong! Game over.")
                valid = False

        elif num == 1:
            if not game2(Time):
                print("Correct! +1")
                score = score + 1
            else:
                print("Wrong! Game over.")
                valid = False
        else:
            if not game3(Time):
                print("Correct! +1")
                score = score + 1
            else:
                print("Wrong! Game over.")
                valid = False

        if score % 5 != 0:
            Time = Time - 5
        
        if Time == 5:
            Time = 5

def game1():#dance recognition

def game2():# voice recognition


def getArtist(promptNum,check,type):#function containing fixed library of prompts for game 3
    #if check is true, then the function will return T/F else return strings

    #the format of the prompt will be question, ans1, ans2, ans3 (semicolons signal next segment and colon signals end)
    questions = ["You are my fire, the one ___;*desire;person;magic","I will always love you:","I will always love you, I will always love ___;food;you;turtles","Clap along if you feel like a room without ___;a roof;some loot;music:"]
    cor = 0
    if(check == False):
        prompt = questions[promptNum]
        val = []
        for char in prompt:
            if char == ';':
                break
            
            val.append(char)

        
        return ''.join(val)
            
    else:
        parsed = parser(questions[promptNum])
       
        for i in range(3):
            curr = parsed[i]
            if curr[0] == '*':
                cor = i
                break
        
        if cor+1 == type:
            return True
        else:
            return False
            


def parser(sentence):
    
    x = 0
    k = 0
    info = []
    for i in range(len(sentence)):
        x = x + 1

        if sentence[i] == ';':
            info.append(sentence[:x-1])
            x=0
            k = k + 1
        
    return info  

def setGPIO():
    GPIO.setmode(GPIO.BCM)
    
    ANS1 = 17
    ANS2 = 27
    ANS3 = 22

    GPIO.setup(ANS1,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(ANS2,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(ANS3,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    
def game3(x):
    #x dictates how long the player has to answer, the time will decrease as the player answers rounds correctly
    
    setGPIO()#configure GPIO
    
    num = random.randint(0,49)
    
    questions = getArtist(num,False,0)
    
    counter = 0
    
    while counter < x:
        ANS1 = GPIO.input(17)
        ANS2 = GPIO.input(27)
        ANS3 = GPIO.input(22)
    
    if((ANS1 == 1 and ANS2 == 1) or (ANS1 == 1 and ANS3 == 1) or (ANS2 == 1 and ANS3 == 1) or (ANS1 == 0 and ANS2 == 0 and ANS3 == 0) or (ANS1 == 1 and ANS2 == 1 and ANS3 == 1)): #error checking
        return False
    else:
        if(ANS1 == 1):
            GPIO_res = 1
        elif(ANS2 == 1):
            GPIO_res = 2
        else:
            GPIO_res = 3
    
    result = getArtist(num,True,GPIO_res)
    
    cleanGPIO()
    
    return result
    
    
def cleanGPIO():
    GPIO.cleanup()
    
    
    
        

