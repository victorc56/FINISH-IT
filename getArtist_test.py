
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

def main():

    question = getArtist(0,False,0)
    print(question)

    result = getArtist(0,True,0)

    print(result)


if __name__ == "__main__":
    main()