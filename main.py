import face_recognition
import os
import cv2
import time
import re
import numpy as np

KNOWN_FACES = "known"
# UNKNOWN_FACES = "unknown"
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"  # hog

video = cv2.VideoCapture(0)

print('loading known faces')

known_face = []
known_name = []

for name in os.listdir(KNOWN_FACES):
    for filename in os.listdir(f'{KNOWN_FACES}/{name}'):
        image = face_recognition.load_image_file(f"{KNOWN_FACES}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]

        known_face.append(encoding)
        known_name.append(name)

print('processing unknown faces')

# for filename in os.listdir(UNKNOWN_FACES):


# import tensorflow.keras as keras
# import tensorflow as tf
# import numpy as np

face_kind = ["real", "fake"]
# new_model = tf.keras.models.load_model('./animal_detector')
# print(new_model.summary())


def find_face_and_recognize():
    while True:
        ret, image = video.read()
        locations = face_recognition.face_locations(image, model=MODEL)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        number_of_face = 0

        for index, face_location in zip(range(len(locations)), locations):

            height = face_location[1] - face_location[3]

            if height > 150:

                number_of_face = number_of_face + 1

                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])

                color = [0, 255, 0]

                cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2] + 22)

                if number_of_face == 1:
                    encodings = face_recognition.face_encodings(image, locations)
                    results = face_recognition.compare_faces(known_face, encodings[index], TOLERANCE)
                    match = None
                    if True in results:
                        match = known_name[results.index(True)]
                        cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                        cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (255, 255, 255), FONT_THICKNESS)
                        # print('تشخیص داده شد')
                        #
                        # return


                else:
                    print('لظفا فقط یک چهره در کادر باشد')

        image2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # new_array = cv2.resize(image, (100, 100))
        # X = [new_array]
        # X_train = np.array(X).reshape(-1, 100, 100, 3)
        # X_train = tf.keras.utils.normalize(X_train, axis=1)
        # predictions = new_model.predict(X_train)
        # cv2.putText(image, face_kind[np.argmax(predictions[0])], (300, 300),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             0.5,
        #             (255, 255, 255), FONT_THICKNESS)

        cv2.imshow('video', image2)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


find_face_and_recognize()
