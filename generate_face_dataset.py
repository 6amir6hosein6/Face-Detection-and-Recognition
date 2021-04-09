import face_recognition
import os
import cv2
import time
import re
import numpy as np

FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"  # hog

video = cv2.VideoCapture(0)

print('loading faces faces')


def find_face_and_recognize():
    p = 0

    while True:
        p = p + 1
        ret, image = video.read()
        locations = face_recognition.face_locations(image, model=MODEL)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        number_of_face = 0

        for index, face_location in zip(range(len(locations)), locations):

            height = face_location[1] - face_location[3]

            if height > 150:
                number_of_face = number_of_face + 1

                crop_img = image[face_location[0]:face_location[2], face_location[3]:face_location[1]]

                crop_img2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imwrite('dataset/fake2/jjj' + str(p) + '.jpg', crop_img2)

        image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imshow('video', image2)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


find_face_and_recognize()
