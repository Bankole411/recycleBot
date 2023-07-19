#!/usr/bin/env python3

import cv2, time, io, picamera
import numpy as np
from recycleBot.actuators.motor import Motor
from recycleBot.yolo.yolo import YOLOWrapper
from recycleBot.sensors.ultra import Ultrasonic

class bottleFollower:
    def __init__(self, camera = None):
        self.ultrasonic = Ultrasonic()
        self.camera = camera
        
        if self.camera:
            self.im_height = self.camera.im_height
            self.im_width = self.camera.im_width
            self.thresh = self.camera.im_width/12
            self.left_thresh = self.camera.im_width/2 - self.thresh
            self.right_thresh = self.camera.im_width/2 + self.thresh
            print(f"{self.thresh} {self.left_thresh} {self.right_thresh}")
            self.PWM = Motor

        self.yolo = YOLOWrapper(self.camera)

    


    def loop(self):
        print("Bottle_button and server route is working")
        if not self.camera:
            return
        try:
            self.process_img(self.yolo.save_frame())
            return 1

        except Exception as e:
            print(e)
            print ("End transmit ... " )
            return -1


    def run(self):
        if not self.camera:
            return
        while True:
            if self.loop() == -1:
                return


    def run_thread(self, exit_handler):
        if not self.camera:
            return
        while True:
            if not exit_handler.is_set():
                return
            if self.loop() == -1:
                return



    def get_overlay(self, frame):
        
        #its too slow, just return the frame
        return frame
        try:
            cx, cy = self.yolo.save_frame(frame)
            frame = cv2.circle(frame, (cx,cy), 20, (0,255,0), -1)
        except:
            pass
        return frame
        
    def check_distance_with_interval(self, interval=0.5):
        while True:
            self.distance = self.ultrasonic.checkdist()
            if self.distance <= 0.3:
                self.PWM.motorStop()   
                print("Distance:", self.distance, "cm")
                time.sleep(interval)

    def process_img(self, ls):
        if not self.camera:
            return
        ls = self.yolo.save_frame()
        return ls

