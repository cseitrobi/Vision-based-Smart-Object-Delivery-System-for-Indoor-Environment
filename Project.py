#! /usr/bin/python

# import the necessary packages

from gpiozero import Servo
from time import sleep
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
flagpin = 18
GPIO.setup(flagpin,GPIO.OUT)
GPIO.output(flagpin,GPIO.LOW)
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # Serial Initialization use your own port befor running
# you will need to change '/dev/ttyACM0' part with your own
servo = Servo(17)
servo.value = 1
cap = cv2.VideoCapture(0)

def recognise_face():
    face_detected = False
    detected_face_name = None
    # Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    # Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())

    # initialize the video stream and allow the camera sensor to warm up
    # Set the ser to the followng
    # src = 0 : for the build in single web cam, could be your laptop webcam
    # src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
    # vs = VideoStream(src=2,framerate=10).start()
    #vs = VideoStream(usePiCamera=True).start()
    
    time.sleep(2.0)

    # start the FPS counter
    #fps = FPS().start()

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        _,frame = cap.read()
        frame = imutils.resize(frame, width=100)
        # Detect the fce boxes
        boxes = face_recognition.face_locations(frame)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"  # if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                # If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    print(currentname)
                    face_detected = True
                    detected_face_name = name
                    

            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        .8, (0, 255, 255), 2)

        # display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

        # quit when 'q' key is pressed
        # if key == ord("q"):
        if face_detected:
            break

        # update the FPS counter
        #fps.update()

    # stop the timer and display FPS information
    #fps.stop()
    #print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    #vs.stop()
    return face_detected, detected_face_name


def start_qr_scan():
    qr_scanned = False
    #cap = cv2.VideoCapture(0)
    found_data = None

    # QR code detection Method
    detector = cv2.QRCodeDetector()
    #print("DEBUG FLAG 1")
    # This creates an Infinite loop to keep your camera searching for data at all times
    while True:

        # Below is the method to get a image of the QR code
        _, img = cap.read()
        img = imutils.resize(img, width=300)
        bbox = None
        #print("DEBUG FLAG 2")
        # Below is the method to read the QR code by detetecting the bounding box coords and decoding the hidden QR data
        data, bbox, _ = detector.detectAndDecode(img)
        #print("DEBUG FLAG 3")
        # This is how we get that Blue Box around our Data. This will draw one, and then Write the Data along with the top (Alter the numbers here to change the colour and thickness of the text)
        if (bbox is not None):

            for i in range(len(bbox)):
                coords = bbox[i]
                for j in range(0, len(coords)):
                    pt1 = (int(coords[j][0]), int(coords[j][1]))
                    pt2 = (int(coords[(j + 1) % len(coords)][0]), int(coords[(j + 1) % len(coords)][1]))
                    cv2.line(img, pt1, pt2, color=(255, 0, 0), thickness=2)

            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 250, 120), 2)

            # Below prints the found data to the below terminal (This we can easily expand on to capture the data to an Excel Sheet)
            # You can also add content to before the pass. Say the system reads red it'll activate a Red LED and the same for Green.
            if data:
                print("data found: ", data)
                found_data = data
                qr_scanned = True
        #print("DEBUG FLAG 4")
        # Below will display the live camera feed to the Desktop on Raspberry Pi OS preview
        cv2.imshow("code detector", img)

        # At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
        if (cv2.waitKey(1) == ord("q") or qr_scanned):
            break

    # When the code is stopped the below closes all the applications/windows that the above has created
    cv2.destroyAllWindows()
    return qr_scanned, found_data
'''
def arduinoreturn(toSend,given):
    
    ser.reset_input_buffer()
    while True:
        toSend += "\n"
        ser.write(toSend.encode('utf-8'))
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if line == given:
                break
            sleep(.25)
'''
# Runner code
while True:
    _, name = recognise_face()
    print('Face Recognised:', name)
    
    #arduinoreturn("p","Face Detected")
    GPIO.output(flagpin,GPIO.HIGH)
    sleep(.5)
    
    print('Looking for QR Code')
    _, data = start_qr_scan()
    print('Data Found:', data)
    sleep(.5)
    
    servo.value = 1
    sleep(.5)
    
    if name == data:
        servo.value = -1
        sleep(2)
        servo.value = 1
        sleep(.5)
        
    
    print('Continue LFR')
    
    GPIO.output(flagpin,GPIO.LOW)
    #arduinoreturn("f","LFR on")
    sleep(.5)
    if (cv2.waitKey(1) == ord("q")):
        break
cap.release()
