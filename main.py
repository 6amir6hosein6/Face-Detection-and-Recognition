import face_recognition
import cv2
import os
import sys
import threading
import time
import numpy as np
import urllib.request
from PyQt5 import QtWidgets
# from Diologs import noWifi, asking_for_confirmation
import freenect
import frame_convert2
from save_new_faces import getting_new_faces
import led_control
from open_door import open_door

dialog_wifi = None
dialog_confirmation = None

Users = "faces"

TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"  # hog

known_face = []
known_name = []

rgb_camera = cv2.imread('start.jpeg')
depth_camera = cv2.imread('start.jpeg')
t1 = None
found = False
match = None
cascade = cv2.CascadeClassifier('cascade.xml')


def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


def real_face_detecter():

    global depth_camera
    rectangles = cascade.detectMultiScale(depth_camera)
    return len(rectangles)


def face_loading():
    for name in os.listdir(Users):
        for filename in os.listdir(f'{Users}/{name}'):
            image = face_recognition.load_image_file(f"{Users}/{name}/{filename}")
            try:
                encoding = face_recognition.face_encodings(image)[0]

                known_face.append(encoding)
                known_name.append(name)
            except:
                pass


def face_detection():
    global rgb_camera, found
    while True:
        if not found:
            #time.sleep(0.1)
            try:
                faces = face_recognition.face_locations(rgb_camera, model=MODEL)
                number_of_face = len(faces)
                #number_of_face = 1
                
                number_of_real_face = real_face_detecter()
                #number_of_real_face = 1
                #print(number_of_face, number_of_real_face)

                if number_of_face == 1 and number_of_real_face >= 1:
                    recognize_face(rgb_camera, faces)
                elif number_of_face == 1 and number_of_real_face <1 :
                    led_control.turn_on_red()
                    led_control.turn_off_blue()
                    time.sleep(2)
                    led_control.turn_off_red()
            except:
                pass

def recognize_face(frame, locations):
    for index, face_location in zip(range(len(locations)), locations):

        height = face_location[1] - face_location[3]

        if height > 50:
            
            encodings = face_recognition.face_encodings(frame, locations)
            results = face_recognition.compare_faces(known_face, encodings[index], TOLERANCE)
            
            if True in results:
                print('here')
                global found, match, rgb_camera
                found, match = True, known_name[results.index(True)]
                rgb_camera = cv2.imread('start.jpeg')
                
            else:
                led_control.turn_on_red()
                led_control.turn_off_blue()
                time.sleep(2)
                led_control.turn_off_red()


def camera_starting():
    global found, match, rgb_camera, depth_camera
    while True:
        if found:
            led_control.turn_on_blue()
            open_door()
            found = False
            match = None
            rgb_camera = cv2.imread('start.jpeg')
            time.sleep(5)
            led_control.turn_off_blue()
        try:
            rgb_camera = cv2.imread('Video.jpg')
            depth_camera = cv2.imread('Depth.jpg')

            cv2.imshow('video', rgb_camera)
        except:
            pass
        if cv2.waitKey(10) == 27:
            break


if __name__ == "__main__":
    # video = cv2.VideoCapture(0)
    #app = QtWidgets.QApplication(sys.argv)

    #getting_new_faces()
    led_control.turn_on_red()
    led_control.turn_on_blue()
    print('-----------')
    print('Loading faces ...')
    face_loading()
    print('Done!')
    led_control.turn_off_red()
    led_control.turn_off_blue()
    
    t1 = threading.Thread(target=face_detection)
    t1.start()

    camera_starting()
