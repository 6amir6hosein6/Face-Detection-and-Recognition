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

print('Start getting image ... ')
while 1:
    cv2.imwrite('Depth.jpg', get_depth())
    cv2.imwrite('Video.jpg', get_video())
    time.sleep(0.5)
    if cv2.waitKey(10) == 27:
        break
