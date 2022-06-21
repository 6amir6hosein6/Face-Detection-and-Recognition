import face_recognition
import cv2
import os
import sys
import threading
import time
import numpy as np
import urllib.request
from PyQt5 import QtWidgets
import socket_control
import freenect
import frame_convert2
from save_new_faces import getting_new_faces
import led_control
from open_door import open_door,close_door
import json
import re
from add_history import add_history
from skimage import io


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
detected = None
pause = False
access = []
cascade = cv2.CascadeClassifier('cascade.xml')

socket_called = [0,0]

def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])


def real_face_detecter():

    global depth_camera
    rectangles = cascade.detectMultiScale(depth_camera)
    return len(rectangles)


def face_loading():
    global access,known_face,known_name
    
    known_face = []
    known_name = []

    close_door()
    led_control.turn_on_red()
    led_control.turn_on_blue()
    print('-----------')
    print('Loading faces ...')
    for name in os.listdir(Users):
        for filename in os.listdir(f'{Users}/{name}'):
            image = face_recognition.load_image_file(f"{Users}/{name}/{filename}")
            try:
                encoding = face_recognition.face_encodings(image)[0]

                known_face.append(encoding)
                known_name.append(name)
            except:
                pass
    t1 = threading.Thread(target=face_detection)
    t1.start()
    print('Done!')
    led_control.turn_off_red()
    led_control.turn_off_blue()
    access = []
    with open('access.json') as f:
        access = json.load(f)


def face_detection():
    global rgb_camera, found,pause
    while not pause:
        if not found:
            try:
                faces = face_recognition.face_locations(rgb_camera, model=MODEL)
                number_of_face = len(faces)
                number_of_real_face = real_face_detecter()

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
    global detected_image
    
    for index, face_location in zip(range(len(locations)), locations):

        height = face_location[1] - face_location[3]

        if height > 50:
            top_left = (max(face_location[3]-60,0),max(face_location[0]-95,0))
            bottom_right = (min(face_location[1]+25,len(frame[0])),min(face_location[2]+35,len(frame
                                                                                               
                                                                                               )))
            detected_image = frame[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
            
            encodings = face_recognition.face_encodings(frame, locations)
            results = face_recognition.compare_faces(known_face, encodings[index], TOLERANCE)
            
            if True in results:
                global found, match, rgb_camera
                found, match = True, known_name[results.index(True)]
                rgb_camera = cv2.imread('start.jpeg')
                
            else:
                led_control.turn_on_red()
                led_control.turn_off_blue()
                time.sleep(2)
                add_history(-1,3,detected_image,socket_called)
                led_control.turn_off_red()


def camera_starting():
    global found, match, detected_image, rgb_camera, depth_camera, t1, pause
    while True:
        time.sleep(0.1)
        if socket_called[0]:
            pause = True
            known_face = []
            known_name = []
            waiting_image = cv2.imread('waiting.jpeg')
            cv2.imshow('video', waiting_image)
            cv2.waitKey(10)
            while socket_called[0]: pass
            pause = False
            face_loading()
            
        
        if found:
            user_id = re.sub(r"(\(.+\))", "", match)
            if access[user_id]:
                
                pause = True
                led_control.turn_on_blue()
                open_door_image = cv2.imread('open-door.jpeg')
                cv2.imshow('video', open_door_image)
                cv2.waitKey(10)
                add_history(user_id,1,detected_image,socket_called)
                open_door()
                led_control.turn_off_blue()
                
            else:
                pause = True
                led_control.turn_on_red()
                open_door_image = cv2.imread('waiting.jpeg')
                cv2.imshow('video', open_door_image)
                cv2.waitKey(10)
                add_history(user_id,2,detected_image,socket_called)
                led_control.turn_off_red()
                
            found = False
            match = None
            time.sleep(5)
            pause = False
            t1 = None
    
            t1 = threading.Thread(target=face_detection)
            t1.start()
        try:
            rgb_camera = cv2.imread('Video.jpeg')
            depth_camera = cv2.imread('Depth.jpeg')
        
            cv2.imshow('video', rgb_camera)
        except:
            pass
        if cv2.waitKey(10) == 27:
            pause = False
            break


if __name__ == "__main__":
    
    #getting_new_faces()
    close_door()
    led_control.turn_on_red()
    led_control.turn_on_blue()
    
    face_loading()
    
    led_control.turn_off_red()
    led_control.turn_off_blue()
    
    t1 = threading.Thread(target=face_detection)
    t1.start()

    camera_starting()
