#!/usr/bin/env python3

import cv2, time, io, picamera
import numpy as np
from recycleBot.actuators.motor import Motor


class Follower:
    def __init__(self, camera):
        self.camera = camera
        self.thresh = self.camera.im_width/12
        self.left_thresh = self.camera.im_width/2 - self.thresh
        self.right_thresh = self.camera.im_width/2 + self.thresh

        print(f"{self.thresh} {self.left_thresh} {self.right_thresh}")

        self.PWM = Motor


    def loop(self):
        try:
            self.process_img(self.camera.get_frame_matrix())
            return 1 
        except Exception as e:
            print(e)
            print ("End transmit ... " )
            return -1


    def run(self):
        while True:
            if self.loop() == -1:
                return

    def run_thread(self, exit_handler):
        print("Line follower_button and server route is working")
        while True:
            if not exit_handler.is_set():
                return
            if self.loop() == -1:
                return
            

    @classmethod
    def get_overlay(cls, frame):
        rgb = frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)


        #computing moments
        h,w,d = frame.shape
        search_top = int(3*h/4)
        search_bot = search_top + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0

        M = cv2.moments(mask)
        if M['m00'] > 0 :
            cx = int (M['m10']/ M['m00'])
            cy = int (M['m01']/ M['m00'])
            rgb = cv2.circle(rgb, (cx,cy), 20, (255,255,255), -1)

        return rgb


    def process_img(self, image):
        #color filtering
        rgb = image
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lower_yellow = np.array([60, 0, 0])
        upper_yellow = np.array([120, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        #masked = cv2.bitwise_and(image, image, mask=mask)

        #computing moments
        h,w,d = image.shape
        search_top = int(3*h/4)
        search_bot = search_top + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0

        M = cv2.moments(mask)
        if M['m00'] > 0 :
            cx = int (M['m10']/ M['m00'])
            cy = int (M['m01']/ M['m00'])

            #follow the dot/ publish to cmd_vel
            print(f"CX: {cx}")

            if self.left_thresh< cx <self.right_thresh:
                self.PWM.backward()
                time.sleep(1.3)
                self.PWM.motorStop()

            elif cx <= self.left_thresh:
                self.PWM.backwardLeft()
                time.sleep(1.3)
                self.PWM.motorStop()

            else:
                self.PWM.backwardRight()
                time.sleep(1.3)
                self.PWM.motorStop()

        cv2.waitKey(3)
        return 

