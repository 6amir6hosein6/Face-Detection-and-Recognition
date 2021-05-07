import face_recognition
import cv2
import requests
import json
import os
import base64
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from ui.wifi import Ui_wifi
from ui.Confirmation import Ui_confirmation
import threading
import time
import re
from functools import partial
import Url

dialog_wifi = None
dialog_confirmation = None

Users = "faces"

TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"  # hog

known_face = []
known_name = []

video_screen = cv2.imread('start.jpeg')
t1 = None
found = False
match = None


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
    global video_screen, found
    while True:
        if not found:
            time.sleep(1)
            faces = face_recognition.face_locations(video_screen, model=MODEL)
            number_of_face = len(faces)
            if number_of_face == 1:
                recognize_face(video_screen, faces)


def recognize_face(frame, locations):
    for index, face_location in zip(range(len(locations)), locations):

        height = face_location[1] - face_location[3]

        if height > 50:

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0, 255, 0]
            cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

            encodings = face_recognition.face_encodings(frame, locations)
            results = face_recognition.compare_faces(known_face, encodings[index], TOLERANCE)

            if True in results:
                global found, match, video_screen
                found, match = True, known_name[results.index(True)]
                video_screen = cv2.imread('start.jpeg')


def camera_starting(video):
    global found, match
    while True:
        if found:
            asking_for_confirmation(match)

        ret, frame = video.read()

        global video_screen
        video_screen = frame.copy()

        cv2.imshow('video', video_screen)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def saving_new_faces(users):
    for user in users:
        name = user['firstName'] + ' ' + user['lastName']
        folder = user['uuId'] + '(' + name + ')'
        path = os.path.join('faces', folder)
        if not os.path.exists('faces/' + folder):
            os.makedirs(path, mode=0o777)

            newfile = base64.b64decode(user['newImage'])

            filename = 'faces/' + folder + '/' + name + '.jpg'
            with open(filename, 'wb') as f:
                f.write(newfile)


def getting_new_faces():
    try:
        url = Url.base + Url.get_new_faces

        response_json = requests.get(url)

        response_data = json.loads(response_json.text)

        saving_new_faces(response_data['data'])

    except:
        noWifi()


def noWifi():
    global dialog_wifi
    dialog_wifi = QtWidgets.QDialog()
    dialog_wifi.ui = Ui_wifi()

    dialog_wifi.ui.setupUi(dialog_wifi)

    dialog_wifi.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dialog_wifi.exec_()


def confirmation(uuid):
    print(uuid)
    try:
        url = Url.base + Url.confirmation
        data = {
            'uuid': uuid,
        }
        requests.post(url, data=data)
    except:
        noWifi()
    dialog_confirmation.close()


def unconfirmation():
    dialog_confirmation.close()


def asking_for_confirmation(info):
    global match, found, dialog_confirmation
    match, found = None, False

    name = re.search("\((.+)\)", info)[1]
    uuid = re.sub(r"(\(.+\))", "", info)

    dialog_confirmation = QtWidgets.QDialog()
    dialog_confirmation.ui = Ui_confirmation()

    dialog_confirmation.ui.setupUi(dialog_confirmation)

    dialog_confirmation.ui.name.setText(name)

    dialog_confirmation.ui.confim.clicked.connect(partial(confirmation, uuid=uuid))
    dialog_confirmation.ui.unconfirm.clicked.connect(partial(unconfirmation))

    dialog_confirmation.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    dialog_confirmation.exec_()


if __name__ == "__main__":
    video = cv2.VideoCapture(0)
    app = QtWidgets.QApplication(sys.argv)

    getting_new_faces()

    face_loading()

    t1 = threading.Thread(target=face_detection)
    t1.start()

    camera_starting(video)
