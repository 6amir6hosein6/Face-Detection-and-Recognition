import cv2
import time
import cv2
import mss
import numpy

cascade = cv2.CascadeClassifier('cascade/cascade.xml')

# while True:
#     image = cv2.imread('positive/face4800.jpg')
#
#     rectangles = cascade.detectMultiScale(image)
#
#     for rectangle in rectangles:
#         start_point = (rectangle[0], rectangle[1])
#         end_point = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
#         color = (255, 0, 0)
#         thickness = 2
#         image = cv2.rectangle(image, start_point, end_point, color, thickness)
#
#     cv2.imshow('face', image)
#
#     cv2.waitKey(1)

with mss.mss() as sct:
    monitor = {'top': 420, 'left': 800, 'width': 450, 'height': 300}
    p = 0
    vid = cv2.VideoCapture(0)

    while 'Screen capturing':
        last_time = time.time()
        img = numpy.array(sct.grab(monitor))
        ret, frame = vid.read()

        rectangles = cascade.detectMultiScale(img)
        for rectangle in rectangles:
            start_point = (rectangle[0], rectangle[1])
            end_point = (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3])
            color = (255, 0, 0)
            thickness = 2
            img = cv2.rectangle(img, start_point, end_point, color, thickness)

        frame = cv2.resize(frame, (450, 300))

        cv2.imshow('OpenCV/Numpy normal', img)
        cv2.imshow('frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()
