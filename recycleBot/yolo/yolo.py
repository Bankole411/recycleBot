import os
import cv2
import time
import shutil

class YOLOWrapper:
    def __init__(self, camera):
        self.inference_path = "/home/pi/recycleBot_master/recycleBot/camera_frames"
        self.label_folder = "/home/pi/recycleBot_master/recycleBot/bottle-classifier/yolov5/runs/detect"
        self.weightsPath = "/home/pi/recycleBot_master/recycleBot/bottle-classifier/yolov5/runs/train/exp3/weights/best.pt"
        self.detectPyPath = "/home/pi/recycleBot_master/recycleBot/bottle-classifier/yolov5/detect.py"
        self.camera = camera
        self.frame_count = 0
        self.frame_interval = 0.5
        self.save_dir = "/home/pi/recycleBot_master/recycleBot/camera_frames"
        self.last_save_time = time.time()
        self.last_centroid_save = [False, False]

    def save_frame(self):
        if self.save_dir is None:
            return None

        frame = self.camera.get_frame_matrix()

        os.makedirs(self.save_dir, exist_ok=True)

        filename = f"frame_{self.frame_count}.jpg"
        filepath = os.path.join(self.save_dir, filename)

        cv2.imwrite(filepath, frame)

        current_time = time.time()
        if current_time - self.last_save_time >= self.frame_interval:
            self.last_centroid_save = self.run_model(filepath)
            self.last_save_time = current_time
            return self.last_centroid_save

        return None

    def run_model(self, filepath):
        exp_folder = self.get_latest_exp_folder()
        label_folder = os.path.join(self.label_folder, exp_folder, "labels")
        command = f'sudo -u pi python {self.detectPyPath} --weights {self.weightsPath} --source {filepath} --save-txt'
        os.system(command)
        return self.get_bottle_image()

    def get_latest_exp_folder(self):
        base_dir = "/home/pi/recycleBot_master/recycleBot/bottle-classifier/yolov5/runs/detect"
        exp_folders = [f for f in os.listdir(base_dir) if f.startswith('exp') and os.path.isdir(os.path.join(base_dir, f))]
        exp_numbers = []

        for folder in exp_folders:
            try:
                exp_number = int(folder[3:])
                exp_numbers.append(exp_number)
            except ValueError:
                pass

        latest_exp_number = max(exp_numbers) if exp_numbers else 0
        return f"exp{latest_exp_number}"

    # def get_bottle_centroid(self):
        # exp_folder = self.get_latest_exp_folder()
        # label_path = os.path.join(self.label_folder, exp_folder, "labels", f"frame_0.txt")
        # img_path = os.path.join(self.label_folder, exp_folder, f"frame_0.jpg")
        # last_bottle_img = img_path
        
        
        # if label_path and os.path.exists(label_path):  # Check if label_path is not None and file exists
            # print(f'Image path: {last_bottle_img}')
            # return last_bottle_img

        # return None
        
    def check_if_bottle(self, file):
        with open(file, 'r') as file:
            for line in file:
                if line.startswith('39'):
                    return True
                return

    def copy_to_static_folder(self, image_path, label_path):
        static_folder = "/home/pi/recycleBot_master/static"
        if self.check_if_bottle(label_path):
            shutil.copy2(image_path, static_folder)
            print("image copied")
        
    def get_bottle_image(self):
        label_folder = "/home/pi/recycleBot_master/recycleBot/bottle-classifier/yolov5/runs/detect"
        exp_folder = self.get_latest_exp_folder()
        image_path = os.path.join(label_folder, exp_folder, f"frame_0.jpg")
        label_path = os.path.join(label_folder, exp_folder, "labels/frame_0.txt")
        self.copy_to_static_folder(image_path, label_path)
