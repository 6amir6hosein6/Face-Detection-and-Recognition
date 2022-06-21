#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import time

#cv2.namedWindow('Depth')
#cv2.namedWindow('Video')
print('Press ESC in window to stop')


def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])

waiting = cv2.imread('waiting.jpeg')
cv2.imwrite('Video.jpeg', waiting)
print('Start getting image ... ')
while 1:
    try:
        cv2.imwrite('Depth.jpeg', get_depth())
        cv2.imwrite('Video.jpeg', get_video())
    except:
        waiting = cv2.imread('waiting.jpeg')
        cv2.imwrite('Video.jpeg', waiting)
    time.sleep(0.5)
    if cv2.waitKey(10) == 27:
        break
