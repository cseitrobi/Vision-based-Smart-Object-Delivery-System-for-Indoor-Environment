import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 18
GPIO.setup(pin,GPIO.OUT)

GPIO.output(pin, GPIO.HIGH)
time.sleep(5)
GPIO.output(pin, GPIO.LOW)
GPIO.cleanup
