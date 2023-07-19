import RPi.GPIO as GPIO
import time 
from recycleBot.actuators.motor import Motor
import threading
# The output pins of the hunting module


'''
Initialize your GPIO port related to the line patrol module
''' 
    
class Line_Tracking(threading.Thread):
    def __init__(self):
        #GPIO pins for output (tracking module)
        self.line_pin_right = 19
        self.line_pin_middle = 16
        self.line_pin_left = 20
        self.Dir_forward = 0
        self.Dir_backward = 1
        self.left_forward = 1
        self.left_backward = 0
        self.right_forward = 0
        self.right_backward= 1
    
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.line_pin_right,GPIO.IN)
        GPIO.setup(self.line_pin_middle,GPIO.IN)
        GPIO.setup(self.line_pin_left,GPIO.IN)
        #motor.setup()
        
        self.mark = 0
        self.PWM = Motor
    
    def trackLineProcessing(self): 
        try:
            self.status_right = GPIO.input(self.line_pin_right)
            self.status_middle = GPIO.input(self.line_pin_middle)
            self.status_left = GPIO.input(self.line_pin_left)
            global mark
            if self.status_left ==0 and self.status_middle == 1 and self.status_right ==0:# (0 1 0)
                self.PWM.motor_left(1, self.left_forward, 80) # self.PWM.motor_left(status, self.left_forward, speed) status:1 means action, 0 means end. self.left_forward:Left motor forward. speed: motor speed. 
                self.PWM.motor_right(1, self.right_forward, 80)# self.right_forward: Right motor forward
                self.mark = 1
            elif self.status_left ==1 and self.status_middle == 1 and self.status_right ==0:# (1 1 0 )
                if self.mark !=2: 
                    self.PWM.motor_left(1, self.left_backward, 80) # self.left_backward: Left motor backward
                    self.PWM.motor_right(1, self.right_backward, 80) # self.right_backward: Right motor backward
                    time.sleep(0.03)
                    self.PWM.motor_left(1, self.left_forward, 70)
                    self.PWM.motor_right(1, self.right_forward, 100)
                    self.mark = 2

            elif self.status_left ==1 and self.status_middle == 0 and self.status_right ==0:#(1 0 0)
                if self.mark !=3: 
                    self.PWM.motor_left(1, self.left_backward, 80)
                    self.PWM.motor_right(1, self.right_backward, 80)
                    time.sleep(0.03)
                    self.PWM.motor_left(1, self.left_forward, 0)
                    self.PWM.motor_right(1, self.right_forward, 100)
                    time.sleep(0.02)
                    self.mark = 3
            elif self.status_left ==0 and self.status_middle == 1 and self.status_right ==1:# (0 1 1)
                if self.mark !=4: 
                    self.PWM.motor_left(1, self.left_backward, 80)
                    self.PWM.motor_right(1, self.right_backward, 80)
                    time.sleep(0.03)
                    self.PWM.motor_left(1, self.left_forward, 100)
                    self.PWM.motor_right(1, self.right_forward, 70)
                    self.mark = 4
            elif self.status_left ==0 and self.status_middle == 0 and self.status_right ==1:# (0 0 1)
                if self.mark !=5: 
                    self.PWM.motor_left(1, self.left_backward, 80)
                    self.PWM.motor_right(1, self.right_backward, 80)
                    time.sleep(0.03)
                    self.PWM.motor_left(1, self.left_forward, 100)
                    self.PWM.motor_right(1, self.right_forward, 0)
                    time.sleep(0.02)
                    self.mark = 5
            else: 
                if self.mark ==0 : 
                    self.PWM.motor_left(1, self.left_forward, 80)
                    self.PWM.motor_right(1, self.right_forward, 80)
                elif self.mark == 1: 
                    self.PWM.motor_left(1, self.left_forward, 80)
                    self.PWM.motor_right(1, self.right_forward, 80)
                elif self.mark == 2 or self.mark == 3: # (1 0 0)
                    self.PWM.motor_left(1, self.left_forward, 0)
                    self.PWM.motor_right(1, self.right_forward, 100)
                    time.sleep(0.03)
                elif self.mark == 4 or self.mark == 5: 
                    self.PWM.motor_left(1, self.left_forward, 100)
                    self.PWM.motor_right(1, self.right_forward, 0)
                    time.sleep(0.03)
                time.sleep(0.1)

        except Exception as e:
            print(e)
            print ("End transmit ... " )
            return -1
        

    def run(self):
        while True:
            if self.trackLineProcessing() == -1:
                return
            

    def run_thread(self, exit_handler): 
        print("Line_tracking run_thread() is working")       
        while True:
            if not exit_handler.is_set():
                print("Line_tracking not getting to logic")
                return
            if self.trackLineProcessing() == -1:
                print("Line_tracking getting to logic")
                return
        print("Line_tracking not True")

if __name__ == '__main__':
    while 1: 
        Line_Tracking().trackLineProcessing()
