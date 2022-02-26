# Raspberry Pi 3B+ Facial Recognition and QR code scan embedded with larduino which is used for line following.
Hardware and software tools
4.1 Design Tools
To implement the project, we have used the following design tools. The design tools include the following list. 
•	Arduino Mega 2560 Microcontroller
•	L293D Motor Driver Shield
•	5 array infrared sensor (IR)
•	Raspberry PI 3 B+ 
•	PI camera:
•	SG-90 servo motor
•	DC-DC buck converter (LM2596 with display
•	Power supply
•	Arduino IDE
•	Thony, Python IDE
•	Linux Terminal in Raspberry PI

Initially, we solder the wires to four dc motors and then connect them to M1, M2, M3 and M4 pins of the L293D motor driver board. Then, place the L293D motor driver over the Arduino mega 2560 board. Then, the connection will be as below automatically –
 
Arduino pin	L293D pin
AREF	AREF
GND	GND
13-0	13-0
RESET	RESET
3.3v	3.3v
5v	5v
GND	GND
Vin	Vin
A0-A7	A0-A7
  
Arduino Pin 	5 Array IR sensor
A8	S1
A9	S2
A10	S3
A11	S4
A12	S5
5v	Vcc
GND	GND
![image](https://user-images.githubusercontent.com/10431781/155857399-5df557d6-d500-42f7-a6d8-6ebc11b95c6c.png)
Fig: Full line following robot setup
4.3.2 Assembling procedure for Raspberry PI with a camera and object delivery box
In this assembling procedure, we attach the camera’s flat cable to the raspberry PI first. Secondly, we connected the servo motor to the raspberry PI and put this servo motor inside the box. After that, this servo motor is responsible for opening the gate of the box. 
![image](https://user-images.githubusercontent.com/10431781/155857410-e89cd6c9-200d-472e-ac5e-f7f6f42e5946.png)
                                             Fig: Object delivery robot with all components



Implementation and Performance analysis
5.1 Experimental setup
We did our experimental setup in several ways. Firstly, we have done our line following part. Secondly, we set up our raspberry pi camera with a raspberry PI and it can detect a face. Here, we took a minimum of 10 pictures of each person for better accuracy and train those images by using the OpenCV built-in function. Thirdly, we scan different QR codes and analyze the timing response to scan them. The next part is, to set up the servo motor and make sure there’s no jitter issue happening. We set up the minimum pulse width, maximum pulse width values in servo motor configuration. And in the final step, we combine Arduino mega board with raspberry PI by connecting PI’s ground pin to Arduino ground pin and Arduino’s analog pin to GPIO18 (12th pin)

5.2.1 Line following Part:
We have installed the “AFmotor.h” library for the L293D motor driver shield. We call the constructor “AF_DCMotor” so that we can select front, back, left, right motors and customize as needed. AF_DCMotor also has a setSpeed() function. We set the speed of the motor 90, so that LFR can move slowly and detect authenticated person’s face. We put the value of the serial monitor to 9600 baud rate. 
In the IR sensor portion, we took the analog value by placing the sensors on a white and black line. Then, we analyzed those values and wrote the code by following the flowchart.

5.2.2 Flowchart for line following:
Initially, 5 array IR sensors will take the reading of all sensors. If the sensor analog value is less than 500, it will count as a black line. If sensor 3 and sensor 4 read value less than 500; or sensor 2 and sensor 3 read value less than 500, then, it will go straight. If sensor 1 and senor 5 read value greater than 500, LFR goes to the straight line. If the value of the middle sensor means sensor 3’s reading value is less than 500, it will go straight. If the right side sensors see a black line, then LFR will go right. And finally, if the left sensors see the black line and the right sensors see the white line, LFR will go left. 

