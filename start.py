from camera_rgb import start_camera as start_rgb
from camera_depth import start_camera as start_depth

from main import main ,amir
import cv2
from multiprocessing import Process, Manager, Pool, Value

waiting = cv2.imread('waiting.jpeg')
cv2.imwrite('Video.jpeg', waiting)

is_end = Value('l', 0)


p1 = Process(target=start_rgb,args=(is_end,))
#p2 = Process(target=start_depth,args=(is_end,))

p3 = Process(target=main,args=(is_end,))

p1.start()
#p2.start()
p3.start()

#p1.join()
#p2.join()


while True:
    print("Any time you want to exit press 'e' ")
    res = input("")
    if res == "e":
        is_end.value = 1
        break
    