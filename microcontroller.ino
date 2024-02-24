


int gamemode = 0; //pi will send this variable over to indicate the input is select the artist. This will be read from digital pin 2.
int counter = 0;//put counter in pi
int choice1 = 5;
int choice2 = 6;
int choice3 = 7;
int choice4 = 8;

void setup() {
  pinMode(2,INPUT);
  pinMode(choice1,INPUT);
  pinMode(choice2,INPUT);
  pinMode(choice3,INPUT);
  pinMode(choice4,INPUT);
}

// the loop function runs over and over again forever
void loop() {
  
  gamemode = digitalRead(2);
  
  //ideas:
  // 4 different digital pins will each represent a multiple choice selection each linked to a different pin on the pi (this will save us on coding logic)
  // the buttons will also link to a finish pin, if the finish pin recieves voltage the selection has been made and this iteration will end
  if(gamemode == 1)//Name the artist has been selected
  {
    if(digitalRead(choice1) == 1)
    {
      //pinMode(choice1,OUTPUT);
      //digitalWrite(choice1,HIGH);
      gamemode = 0;
      digitalWrite 
    }

    pinMode(choice1,INPUT);
  }


  
}
