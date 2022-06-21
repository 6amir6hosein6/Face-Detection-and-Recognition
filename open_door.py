import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)

def open_door():
    GPIO.output(16,GPIO.LOW)
    time.sleep(1)
    GPIO.output(16,GPIO.HIGH)
    
def close_door():
    GPIO.output(16,GPIO.HIGH)

 
