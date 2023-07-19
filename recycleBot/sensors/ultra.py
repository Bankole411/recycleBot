import RPi.GPIO as GPIO
import time
from recycleBot.actuators.motor import Motor 

class Ultrasonic:
    def __init__(self):
        self.triggerPin = 11
        self.echoPin = 8

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.triggerPin, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.echoPin, GPIO.IN)

    def checkdist(self):       #Reading distance
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.triggerPin, GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.output(self.triggerPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.triggerPin, GPIO.LOW)
        while not GPIO.input(self.echoPin):
            pass
        t1 = time.time()
        while GPIO.input(self.echoPin):
            pass
        t2 = time.time()
        return round((t2-t1)*340/2,2)

