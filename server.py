import socket
import time
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
import os
import LED
#from mpu6050 import mpu6050


from flask import Flask, Response, render_template, request, send_file
from recycleBot.camera import VideoCamera
import time, socket, os, threading

from recycleBot.actuators.motor import Motor
#from recycleBot.sensors.adc import ADC
from recycleBot.actuators.servo import Servo
from recycleBot.sensors.ultra import Ultrasonic
from recycleBot.tracking.lineTracking import Line_Tracking
from recycleBot.tracking.line import Follower
from recycleBot.tracking.bottle import bottleFollower
from recycleBot.lights.led import LED
# from recycleBot.tracking.light import Light
from recycleBot.yolo.yolo import YOLOWrapper

from recycleBot.tests.physical import TestPhy


servo_speed  = 11
functionMode = 0
dis_keep = 0.35
goal_pos = 0
tor_pos  = 1
mpu_speed = 2
init_get = 0
scGear = Servo()
scGear.moveInit()

P_sc = Servo()
P_sc.start()

C_sc = Servo()
C_sc.start()

T_sc = Servo()
T_sc.start()

H_sc = Servo()
H_sc.start()

G_sc = Servo()
G_sc.start()

init_pwm = []
for i in range(16):
    init_pwm.append(scGear.initPos[i])

def servoPosInit():
    scGear.initConfig(0,init_pwm0,1)
    P_sc.initConfig(1,init_pwm1,1)
    T_sc.initConfig(2,init_pwm2,1)
    H_sc.initConfig(3,init_pwm3,1)
    G_sc.initConfig(4,init_pwm4,1)


# OLED_connection = 1
# try:
#     import OLED
#     screen = OLED.OLED_ctrl()
#     screen.start()
#     screen.screen_show(1, 'GEWBOT.COM')
# except:
#     OLED_connection = 0
#     print('OLED disconnected\n')
#     pass

# MPU_connection = 1
# try:
#     sensor = mpu6050(0x68)
#     print('mpu6050 connected, PT MODE ON')
#     if OLED_connection:
#         screen.screen_show(4, 'PT MODE ON')
# except:
#     MPU_connection = 0
#     print('mpu6050 disconnected, ARM MODE ON')
#     if OLED_connection:
#         screen.screen_show(4, 'ARM MODE ON')


# servo_speed  = 11
# functionMode = 0
# dis_keep = 0.35
# goal_pos = 0
# tor_pos  = 1
# mpu_speed = 2
# init_get = 0


pi_camera = VideoCamera(flip=False)
app = Flask(__name__)


CURR_MODE = "DEFAULT"


PWM = Motor
#adc = ADC()
pwm = Servo()
_ultrasonic = Ultrasonic()


exit_handler = threading.Event()

threads = {}
thread_states = {
    "line_tracking_is_active" : False,
    "bottle_tracking_is_active" : False,
    "line_following_is_active" : False
}

_test = TestPhy()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


def exec_line_tracking(thread_state_key, thread_name, fn):
    # follow black lines
    Line_Tracking().run_thread(exit_handler)

def exec_line_following(thread_state_key, thread_name, fn):
    #follow yellow line
    Follower(pi_camera).run_thread(exit_handler)
    
def exec_bottle_tracking(thread_state_key, thread_name, fn):
    #follow tracked bottle
    bottleFollower(pi_camera).run_thread(exit_handler)
    



def tracking_handler(thread_state_key, thread_name , fn):
    if thread_states[thread_state_key] == True: #turn it off since its running
        exit_handler.clear()
        pi_camera.mode = "default"
        thread_states[thread_state_key] = False
    else: #turn it on
        exit_handler.set() #disable other tracking routines

        thread_states[thread_state_key] = True
        pi_camera.mode = thread_name
        threads[thread_name] = threading.Thread(target=fn, args=(thread_state_key, thread_name, fn))
        threads[thread_name].start()
        threads[thread_name].join()




# @app.route('/')
# def index():
    # return render_template('index.html') 

def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    
                    
def getting():
    while True:
        with open('/home/pi/recycleBot_master/static/frame_0.jpg', 'rb') as f:
            frame = f.read()

            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/pic_bottle')
def pic_bottle():
    return Response(getting(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test', methods=['POST'])
def test():
    args = {
        'Led':_test.test_led,
        'Motor': _test.test_motors,
        'Ultrasonic': _test.test_ultrasonic,
        'lineTracking': _test.test_line_tracking,
        'Servo': _test.test_servos,
        #'ADC': _test.test_adc,
        #'Buzzer': _test.test_buzzer
    }
    arg = request.form['arg']
    print(f"Testing {arg}")

    if arg == "ALL":
        for k,v in args:
            print(f"Testing {arg}")
            v()
 
    elif arg in args:
        args[arg]()
    
    else:
        print(f"TEST : Argument {arg} does not exist")
    return "Done"

@app.route('/move', methods=['POST'])
def move():
    args = {
        'Forward_LEFT'      : PWM.backwardLeft, 
        'Forward_RIGHT'     : PWM.backwardRight , 
        'FORWARD'   : PWM.backward, 
        'BACKWARDS' : PWM.forward,
        'Backward_LEFT'      : PWM.forwardLeft, 
        'Backward_RIGHT'     : PWM.forwardRight ,  
        'STOP' :  PWM.motorStop
    }
    arg = request.form['arg']
    print(f"Moving : {arg}")

    if arg in args.keys():
        args[arg]()
    else:
        print(f"MOVE : Argument {arg} does not exist")

    return "Done"


@app.route('/servo', methods=['POST'])
def servo():
	def lookleft():
		P_sc.singleServo(0, 1, 3)
		
	def lookright():
		P_sc.singleServo(0, -1, 3)
			
	def LRstop():
		P_sc.stopWiggle()

	def armup():
		T_sc.singleServo(1, 1, 3)

	def armdown():
		T_sc.singleServo(1, -1, 3)

	def armstop():
		T_sc.stopWiggle()

	def handup():
		H_sc.singleServo(2, 1, 3)
		
	def handdown():
		H_sc.singleServo(2, -1, 3)
			
	def handstop():
		H_sc.stopWiggle()

	def grab():
		G_sc.singleServo(3, -1, 3)

	def loose():
		G_sc.singleServo(3, 1, 3)

	def cameraup():
		C_sc.singleServo(4, 1, 3)

	def cameradown():
		C_sc.singleServo(4, -1, 3)
			
	def camerastop():
		C_sc.stopWiggle()
		
	def stop():
		G_sc.stopWiggle()
		P_sc.stopWiggle()
		C_sc.stopWiggle()
		H_sc.stopWiggle()
		T_sc.stopWiggle()

	def home():
		P_sc.moveServoInit([0])
		C_sc.moveServoInit([4])
		T_sc.moveServoInit([1])
		H_sc.moveServoInit([2])
		G_sc.moveServoInit([3])
		
	args = {
		'ARM-UP' :  lambda: armup(), 
		'ARM-DOWN' : lambda: armdown(), 
		'LEFT' :    lambda: lookleft(), 
		'RIGHT' :  lambda: lookright(), 
		'HAND-UP' :  lambda: handup(), 
		'HAND-DOWN' :  lambda: handdown(), 
		'GRAB' :  lambda: grab(), 
		'LOOSE' :  lambda: loose(), 
		'LOOK-UP' :  lambda: cameraup(), 
		'LOOK-DOWN' :  lambda: cameradown(), 
		'STOP' :  lambda: stop(),
		
	}
	arg = request.form['arg']
	print(f"Moving : {arg}")

	if arg in args.keys():
		args[arg]()
	else:
		print("Argument does not exist")
	return "Done" 


# @app.route('/battery_percentage', methods=['GET'])
# def battery_percentage():
#     adc_power = adc.recvADC(2)*3
#     percent_power= int( (adc_power-7)/1.40*100 )
#     return f"{percent_power}"


@app.route('/ultrasonic', methods=['GET'])
def ultrasonic():
    return f"{_ultrasonic.checkdist()}"



@app.route('/line_tracking', methods=['POST'])
def line_tracking():
    tracking_handler("line_tracking_is_active", "line_tracking", 
        exec_line_tracking)
    return "OK"


@app.route('/line_following', methods=['POST'])
def line_following():
    tracking_handler("line_following_is_active", "line_following", 
        exec_line_following)
        
    return "OK"

@app.route('/bottle_tracking', methods=['POST'])
def bottle_tracking():
    tracking_handler("bottle_tracking_is_active", "bottle_tracking", 
       exec_bottle_tracking)
    return "OK"

    
@app.route('/')
def render_html():
    # Render the index.html template and pass the image path
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host=get_local_ip(), debug=False)
