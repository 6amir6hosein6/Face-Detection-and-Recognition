import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

def turn_on_red():
    GPIO.output(21,GPIO.HIGH)
    
def turn_on_blue():
    GPIO.output(20,GPIO.HIGH)
    
def turn_off_red():
    GPIO.output(21,GPIO.LOW)
    
def turn_off_blue():
    GPIO.output(20,GPIO.LOW)


turn_off_red()
turn_off_blue()

