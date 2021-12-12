#include <Adafruit_MotorShield.h>

#define vinPin A5
#define buz 9
#define pulsePin 3
#define led 10

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61);

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *motor1 = AFMS.getMotor(1);
// You can also make another motor on port M2
Adafruit_DCMotor *motor2 = AFMS.getMotor(2);

int analogPin0 = A0;
int analogPin1 = A1;
int analogPin2 = A2;
int analogPin = A3
int val0 = 0;  // variable to store the value read
int val1 = 0;
int val3 = 0;
int val = 0
int button = 0;
int c;
int non_button = 1;
const int threshold = 15;
const int numReadings = 40;
//TRANSDUCER SENSOR VARIABLES
int trigPin = 9;    // TRIG pin
int echoPin = 8;    // ECHO pin
float duration_us, distance_cm; //DISTANCE VALUES
int DISTANCE_CHECKER = 1; //ON/OFF FOR THE TRANSUDCER
int spin_set = 0;

int readings0[numReadings];  // Number of readings that we will take the average over
int readings1[numReadings];
int readIndex = 0;  // variable that will index us which value we are from 0 --> numReadings
int total0 = 0;  // running total
int total1 = 0;
int average0 = 0; // average that we care about
int average1 = 0;

long sumExpect=0; //running sum of 64 sums 
long ignor=0;   //number of ignored sums
long diff=0;        //difference between sum and avgsum
long pTime=0;
long buzPeriod=0; 


void setup() {
  Serial.begin(9600);           //  setup serial
  if (1 == 0) {
    //initialise the reading to 0#
    for (int thisReading = 0; thisReading < numReadings; thisReading++) {
      readings0[thisReading] = 0;
      readings1[thisReading] = 0;
    }
  } // end of block
  Serial.println("Adafruit Motorshield v2 - DC Motor test!");

  if (!AFMS.begin()) {         // create with the default frequency 1.6KHz
    // if (!AFMS.begin(1000)) {  // OR with a different frequency, say 1KHz
    Serial.println("Could not find Motor Shield. Check wiring.");
    //while (1);
  }
  Serial.println("Motor Shield found.");

  // Set the speed to start, from 0 (off) to 255 (max speed)
  motor1->setSpeed(255);
  motor2->setSpeed(200);
  motor1->run(BACKWARD);
  motor2->run(BACKWARD);
  // turn on motor
  motor1->run(RELEASE);
  motor2->run(RELEASE);

  // Transducer pins
  // configure the trigger pin to output mode
  pinMode(trigPin, OUTPUT);
  // configure the echo pin to input mode
  pinMode(echoPin, INPUT);

  // Metal detector pins
  pinMode(pulsePin, OUTPUT); 
  digitalWrite(pulsePin, LOW);
  pinMode(vinPin, INPUT);  
  pinMode(buz, OUTPUT);
  digitalWrite(buz, LOW);
  pinMode(led, OUTPUT);
}

void loop() {
  val3 = analogRead(analogPin2);
  if (val3 < 10) { //button variable
    button = 1;
    Serial.print(button);
  }
  if (button == 1) { // comment it all out
    val0 = analogRead(analogPin0);  // read the input pins
    val1 = analogRead(analogPin1);

    analogWrite(A2, 1);

    // subtract last reading
    total0 = total0 - readings0[readIndex];
    total1 = total1 - readings1[readIndex];
    //using val from sensors
    readings0[readIndex] = val0;
    readings1[readIndex] = val1;

    //add it to total
    total0 = total0 + readings0[readIndex];
    total1 = total1 + readings1[readIndex];
    //go to next position in list
    readIndex = readIndex + 1;
    //End of Array check
    if (readIndex >= numReadings) {
      readIndex = 0; //This basically shoots it back to the beginning

    }
    //Calculation time
    average0 = total0 / numReadings;
    average1 = total1 / numReadings;

    //Serial.println(average0);
    //Serial.println(average1);

    // white = low, black = high

    if (spin_set == 1) {
      // stop moving, TODO: reverse previous movements until white line found, then follow again
      Serial.println("Stopped");
      motor1->run(RELEASE);
      motor2->run(RELEASE);
      delay(500);
      Serial.println("TURNING");
      //Serial.println(0);
    }
    else if ((average0 > threshold) && (average1 < threshold)) {
      turn_left();
      //Serial.println(-1);
    }
    else if ((average0 < threshold) && (average1 > threshold)) {
      turn_right();
      //Serial.println(1);
    }
    else if ((average0 < threshold) && (average1 < threshold)) {
      go_straight();
      //}

      delay (10);
    } // end of commented out code

  }
  transducer();
  analogWrite(A2, 0)
}
void go_straight()
{
  uint8_t i;

  Serial.println("straight");

  int speed = 255;

  motor1->run(BACKWARD);
  motor2->run(BACKWARD);

  motor1->setSpeed(speed);
  motor2->setSpeed(180);
}

void turn_left()
{
  Serial.println("Left");
  motor1->setSpeed(255);
  motor2->setSpeed(148);
}
void turn_right()
{
  Serial.println("Right");
  motor1->setSpeed(220);
  motor2->setSpeed(198);

}

void transducer()
{
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // measure duration of pulse from ECHO pin
  duration_us = pulseIn(echoPin, HIGH);

  // calculate the distance
  distance_cm = 0.017 * duration_us;

  // print the value to Serial Monitor

  if (distance_cm < 10)
  {
    Serial.print("distance: ");
    Serial.print(distance_cm);
    Serial.println(" cm");
    spin_set = 1;
    Serial.println("hi");
  }

  delay(50);
}

void metal_detection() {

  int minval=1023;
  int maxval=0;
  long unsigned int sum=0;

  for (int i=0; i<256; i++) {

    //reset the capacitor
    pinMode(vinPin,OUTPUT);
    digitalWrite(vinPin,LOW);
    delayMicroseconds(20);
    pinMode(vinPin,INPUT);
    applyPulses();
        
    //read the charge of capacitor
    int val = analogRead(vinPin); //takes 13x8=104 microseconds
    minval = min(val,minval);
    maxval = max(val,maxval);
    sum += val;
        
    long unsigned int cTime=millis();
    char buzState=0;
    
    if (cTime<pTime+10) {
        if (diff>0)
            buzState=1;
        else if(diff<0)
            buzState=2;
    }
    
    if (cTime > pTime + buzPeriod) {
        if (diff>0)
            buzState=1;
        else if (diff<0)
            buzState=2;
            pTime=cTime;   
    }
    
    if (buzPeriod>300)
        buzState=0;

    if (buzState==0) {
        digitalWrite(led, LOW);
        noTone(buz);
    }  
    else if (buzState==1) {
        tone(buz,2000);
        digitalWrite(led, HIGH);
    }
    else if (buzState==2) {
        tone(buz,500);
        digitalWrite(led, HIGH);
    }
    }

    //subtract minimum and maximum value to remove spikes
    sum -= minval; 
    sum -= maxval;
    
    if (sumExpect==0) 
        sumExpect=sum << 6; //set sumExpect to expected value
    
    long int avgsum = (sumExpect + 32) >> 6; 
    diff = sum - avgsum;
    if (abs(diff)<avgsum>>10) {
        sumExpect = sumExpect + sum - avgsum;
        ignor=0;
    } 
    else 
        ignor++;
    
    if (ignor > 64) { 
        sumExpect=sum<<6;
        ignor=0;
    }

    if (diff==0)
        buzPeriod=1000000;
    else 
        buzPeriod=avgsum/(2*abs(diff));    
        val = analogRead(analogPin);  // read the input pin
        Serial.println(val);
    }


void applyPulses() {
    for (int i = 0; i < 3; i++) {
        digitalWrite(pulsePin, HIGH); //take 3.5 uS
        delayMicroseconds(300);
        digitalWrite(pulsePin, LOW);  //take 3.5 uS
        delayMicroseconds(300);
    }
}