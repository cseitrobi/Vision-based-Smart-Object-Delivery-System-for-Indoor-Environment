#include <AFMotor.h>

AF_DCMotor fl(1);

AF_DCMotor fr(3);
AF_DCMotor br(4);
boolean face_found = false;
void setup()
{


  fl.setSpeed(90);

  fr.setSpeed(90);
  br.setSpeed(90);

  pinMode(A15, INPUT);
  Serial.begin(9600);

}

void loop() {
  int flag = analogRead(A15);
  Serial.println(flag);
  //delay(1000);
  if(flag>500) {
    delay(5);
    Serial.println("Face Detected");
    face_found = true;
    fl.run(RELEASE);
    fr.run(RELEASE);
    br.run(RELEASE);
  }
  else {
    face_found = false;
  }

  if (!face_found) {

    Serial.println("LFR on");
    NewFunc();
  }



}

int NewFunc()
{

  int obstacle0 = analogRead(8);
  int obstacle1 = analogRead(9);
  int obstacle2 = analogRead(10);
  int obstacle3 = analogRead(11);
  int obstacle4 = analogRead(12);





  int t = 500;

  if ((obstacle2 < t) && (obstacle3 < t) || (obstacle2 < t) && (obstacle1 < t))
  { //forward
    fl.run(FORWARD);

    fr.run(FORWARD);
    br.run(FORWARD);
  }
  else if ((obstacle4 > t) && (obstacle0 > t))
  {
    //forward
    fl.run(FORWARD);

    fr.run(FORWARD);
    br.run(FORWARD);
  }
  if ((obstacle2 < t))
  { //forward
    fl.run(FORWARD);

    fr.run(FORWARD);
    br.run(FORWARD);
  }
  else if ((obstacle3 < t) || (obstacle4 < t) && (obstacle0 > t))
  { //right
    fl.run(FORWARD);

    fr.run(BACKWARD);
    br.run(BACKWARD);
  }
  else if ((obstacle0 < t) || (obstacle1 < t) && (obstacle4 > t))
  {
    //left
    fl.run(BACKWARD);

    fr.run(FORWARD);
    br.run(FORWARD);
  }


}
