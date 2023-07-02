import os
from recycleBot.camera import VideoCamera
from recycleBot.yolo.yolo import YOLOWrapper


inference_path = "/home/pi/recycleBot_master/recycleBot/camera_frames"
label_folder = "/home/pi/recycleBot_master/recycleBot/bottle-classifier/yolov5/runs/detect/exp10/labels"
camera_obj = VideoCamera(flip=False)
wrapper = YOLOWrapper(inference_path, label_folder, camera_obj, save_dir = save_directory)

print(wrapper.get_bounding_boxes(image_name))
