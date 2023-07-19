import time
import RPi.GPIO as GPIO

# Pin numbers for motor control
Motor_A_EN = 4
Motor_B_EN = 17
Motor_A_Pin1 = 26
Motor_A_Pin2 = 21
Motor_B_Pin1 = 27
Motor_B_Pin2 = 18

# Motor direction constants
Dir_forward = 0
Dir_backward = 1

left_forward = 1
left_backward = 0

right_forward = 0
right_backward = 1

pwm_A = 100
pwm_B = 100

speed = 100

class Motor:
    def motorStop():
        # Stop both motors
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)

    def setup():
        global pwm_A, pwm_B
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        Motor.motorStop()

        # try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)
        # except:
        #     pass

    def motor_left( status, direction, speed):
        if status == 0: # stop
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            GPIO.output(Motor_B_EN, GPIO.LOW)
        else:
            if direction == Dir_backward:
                GPIO.output(Motor_B_Pin1, GPIO.HIGH)
                GPIO.output(Motor_B_Pin2, GPIO.LOW)
                pwm_B.start(100)
                pwm_B.ChangeDutyCycle(speed)
            elif direction == Dir_forward:
                GPIO.output(Motor_B_Pin1, GPIO.LOW)
                GPIO.output(Motor_B_Pin2, GPIO.HIGH)
                pwm_B.start(0)
                pwm_B.ChangeDutyCycle(speed)

    def motor_right(status, direction, speed):#Motor 1 positive and negative rotation
        if status == 0: # stop
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            GPIO.output(Motor_A_EN, GPIO.LOW)
        else:
            if direction == Dir_forward:#
                GPIO.output(Motor_A_Pin1, GPIO.HIGH)
                GPIO.output(Motor_A_Pin2, GPIO.LOW)
                pwm_A.start(0)
                pwm_A.ChangeDutyCycle(speed)
            elif direction == Dir_backward:
                GPIO.output(Motor_A_Pin1, GPIO.LOW)
                GPIO.output(Motor_A_Pin2, GPIO.HIGH)
                pwm_A.start(0)
                pwm_A.ChangeDutyCycle(speed)
        return direction


    def movementModel( speed, direction, turn, radius=0.6):   # 0 < radius <= 1  
        if direction == 'forward':
            if turn == 'right':
                Motor.motor_left(0, left_backward, int(speed*radius))
                Motor.motor_right(1, right_forward, speed)
            elif turn == 'left':
                Motor.motor_left(1, left_forward, speed)
                Motor.motor_right(0, right_backward, int(speed*radius))
            else:
                Motor.motor_left(1, left_forward, speed)
                Motor.motor_right(1, right_forward, speed)
        elif direction == 'backward':
            if turn == 'right':
                Motor.motor_left(0, left_forward, int(speed*radius))
                Motor.motor_right(1, right_backward, speed)
            elif turn == 'left':
                Motor.motor_left(1, left_backward, speed)
                Motor.motor_right(0, right_forward, int(speed*radius))
            else:
                Motor.motor_left(1, left_backward, speed)
                Motor.motor_right(1, right_backward, speed)
        elif direction == 'no':
            if turn == 'right':
                Motor.motor_left(1, left_backward, speed)
                Motor.motor_right(1, right_forward, speed)
            elif turn == 'left':
                Motor.motor_left(1, left_forward, speed)
                Motor.motor_right(1, right_backward, speed)
            else:
                Motor.motorStop()
        else:
            pass

    
    def forward():
        print("Going forward")
        Motor.movementModel(speed, 'forward', '', radius=0.6)

    def forwardRight():
        print("Turning Right")
        Motor.movementModel(speed, 'forward', 'right', radius=0.6)

    def forwardLeft():
        print("Turning Left")
        Motor.movementModel(speed, 'forward', 'left', radius=0.6)

    def backward():
        print("Going Backward")
        Motor.movementModel(speed, 'backward', '', radius=0.6)

    def backwardRight():
        print("Turning Right")
        Motor.movementModel(speed, 'backward', 'right', radius=0.6)

    def backwardLeft():
        print("Turning left")
        Motor.movementModel(speed, 'backward', 'left', radius=0.6)

    def stop():
        print("Stop!")
        Motor.movementModel(0, '', '', radius=0)

def destroy():
	Motor.motorStop()
	GPIO.cleanup() 
        
Motor.setup()

if __name__ == '__main__':
	try:
		Motor.backward()
		time.sleep(3.3)
		Motor.destroy()
	except KeyboardInterrupt:
		Motor.destroy()
