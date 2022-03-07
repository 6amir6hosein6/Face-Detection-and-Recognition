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
# from save_new_faces import getting_new_faces


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

    # color = (255, 0, 0)
    # thickness = 2
    # for rectangle in rectangles:
    #     start_point = (rectangle[0], rectangle[1])
    #     end_point = (rectangle[2]+rectangle[0], rectangle[3]+rectangle[1])
    #     image = cv2.rectangle(image, start_point, end_point, color, thickness)

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
            time.sleep(1)
            faces = face_recognition.face_locations(rgb_camera, model=MODEL)
            number_of_face = len(faces)

            number_of_real_face = real_face_detecter()
            # number_of_real_face = 1

            # print(number_of_face, number_of_real_face)

            if number_of_face == 1 and number_of_real_face >= 1:
                recognize_face(rgb_camera, faces)


def recognize_face(frame, locations):
    for index, face_location in zip(range(len(locations)), locations):

        height = face_location[1] - face_location[3]

        if height > 50:

            # top_left = (face_location[3], face_location[0])
            # bottom_right = (face_location[1], face_location[2])
            # color = [0, 255, 0]
            # cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

            encodings = face_recognition.face_encodings(frame, locations)
            results = face_recognition.compare_faces(known_face, encodings[index], TOLERANCE)

            # color = (255, 0, 0)
            # thickness = 2
            # for rectangle in rectangles:
            #     start_point = (rectangle[0], rectangle[1])
            #     end_point = (rectangle[2]+rectangle[0], rectangle[3]+rectangle[1])
            #     image = cv2.rectangle(image, start_point, end_point, color, thickness)

            if True in results:
                global found, match, rgb_camera
                found, match = True, known_name[results.index(True)]
                rgb_camera = cv2.imread('start.jpeg')


def camera_starting():
    global found, match, rgb_camera, depth_camera
    while True:
        if found:
            print(match)
            # asking_for_confirmation(match)

        rgb_camera = get_video()
        depth_camera = get_depth()

        cv2.imshow('video', rgb_camera)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    # video = cv2.VideoCapture(0)
    app = QtWidgets.QApplication(sys.argv)

    # getting_new_faces()

    print('-----------')
    print('Loading faces ...')
    face_loading()
    print('Done!')

    t1 = threading.Thread(target=face_detection)
    t1.start()

    camera_starting()
