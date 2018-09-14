import RPi.GPIO as GPIO
import time
import colorShape

list1 = []

LedPin_B = 11
LedPin_G = 12
LedPin_R = 13

GPIO.setmode(GPIO.BOARD)         # Numbers GPIOs by physical location
GPIO.setup(LedPin_B, GPIO.OUT)   # Set LedPin's mode as output    
GPIO.setup(LedPin_G, GPIO.OUT)   # Set LedPin's mode as output  
GPIO.setup(LedPin_R, GPIO.OUT)   # Set LedPin's mode as output
    
def blink(color,number):
    global list1
    list1.append(color)
    
    for i in number:  
        if(color == "blue"):
            GPIO.output(LedPin_B, GPIO.HIGH)
            sleep(1)
            GPIO.output(LedPin_B, GPIO.LOW)

        elif(color == "green"):
            GPIO.output(LedPin_G, GPIO.HIGH)
            sleep(1)
            GPIO.output(LedPin_G, GPIO.LOW)

        elif(color == "red"):
            GPIO.output(LedPin_R, GPIO.HIGH)
            sleep(1)
            GPIO.output(LedPin_R, GPIO.LOW)

def blink_shed()
    for i in list1:
        if(i == "blue"):
            GPIO.output(LedPin_B, GPIO.HIGH)
            sleep(1)
            GPIO.output(LedPin_B, GPIO.LOW)

        elif(i == "green"):
            GPIO.output(LedPin_G, GPIO.HIGH)
            sleep(1)
            GPIO.output(LedPin_G, GPIO.LOW)

        elif(i == "red"):
            GPIO.output(LedPin_R, GPIO.HIGH)
            sleep(1)
            GPIO.output(LedPin_R, GPIO.LOW)
