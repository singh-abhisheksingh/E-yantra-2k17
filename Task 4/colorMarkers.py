import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


Motor1A = 33
Motor1B = 35
Motor1E = 37
Motor2A = 36
Motor2B = 38
Motor2E = 40

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

left = GPIO.PWM(Motor1E, 100)
right = GPIO.PWM(Motor2E, 100)
##############################################################################################################

def forward():
    GPIO.output(Motor1A,GPIO.LOW)    
    GPIO.output(Motor1B,GPIO.HIGH)
    left.ChangeDutyCycle(100)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    right.ChangeDutyCycle(100)


def right1():
    GPIO.output(Motor1A,GPIO.LOW)   
    GPIO.output(Motor1B,GPIO.HIGH)
    left.ChangeDutyCycle(100)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    right.ChangeDutyCycle(100)


def left1():
    GPIO.output(Motor1A,GPIO.LOW)   
    GPIO.output(Motor1B,GPIO.LOW)
    left.ChangeDutyCycle(100)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    right.ChangeDutyCycle(100)


##############################################################################################################

contour_area = 0
max_area = 0
contour_index = 0
contour = 0
i = 0

a=[[(110,100,100),(130,255,255)],[(50,100,100),(70,255,255)],[(-10,100,100),(10,255,255)]]
###############################################################################################################

cam = PiCamera()
cam.resolution = (160,120)
cam.framerate = 5
raw_cap = PiRGBArray(cam,(160,120))
frame_cnt = 0
for frame in cam.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(160,120)):
    #time.sleep(1.0)
    #image = frame.next()
    #extract opencv bgr array of color frame
    color_image = frame.array
    #cv2.imshow("Input Video",color_image)
    #cv2.waitKey(1)
################################################################################################################

    img = color_image.copy()
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    #ret,thresh = cv2.threshold(gray,40,255,1)
    _,contours,h = cv2.findContours(thresh,1,2)
    
    i = 0
    max_area = 0
    colour=""
    
    for cnt in contours:

        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        #colour = frame[cy, cx]
        if len(approx)==3:
            colour=col()

        elif len(approx)==4:
            colour=col()

        elif len(approx)>12:
            colour=col()

###############################################################################

     
    def col():
        for i in a:
            lower = np.array(i[0])   
            upper = np.array(i[1])
            if cv2.inRange(hsv, lower, upper):
                return "blue"
            elif cv2.inRange(hsv, lower, upper):
                return "green"
            elif cv2.inRange(hsv, lower, upper):
                return "red"


###############################################################################

    M = cv2.moments(contour)
    if(M['m00'] == 0):
        M['m00'] = 1
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    #print cx,",",cy
################################################################################################################
    
    centroid = "("+str(cx) + "," + str(cy)+")"
    #cv2.putText(img, centroid, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    #cv2.putText(img, "centroid", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    #cv2.circle(img, (cx, cy), 4, (0,0,255), -1)
    
    height, width  = img.shape[:2]
    height = height/2
    width = width/2
    centre = "("+str(width) + "," + str(height)+")"
    #cv2.putText(img, centre, (width, height), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    #cv2.putText(img, "centre", (width+20, height+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
#################################################################################################################

    diff = cx - width
    print diff
    difference = str(diff)
    cv2.putText(img, difference, (width + diff + 10,height + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    cv2.circle(img, (width + diff,height), 4, (0,0,255), -1)
    cv2.circle(img, (width, height), 4, (255,0,0), -1)
    
    cv2.drawContours(img,contours,contour_index,(0,255,0),3)
    cv2.imshow('contour',img)

    if(diff > 25):
        left.start(100)
        right.start(100)
        sleep(0)
        right1()
        sleep(0.1)
        left.stop()
        right.stop()

    elif(diff < -25):
        left.start(100)
        right.start(100)
        sleep(0)
        left1()
        sleep(0.1)
        left.stop()
        right.stop()

    else:
        #move forward
        left.start(100)
        right.start(100)
        sleep(0)
        forward()
        sleep(0.2)
        left.stop()
        right.stop()

            
    if cv2.waitKey(1) == 27:
        break
##################################################################################################################

    raw_cap.truncate(0)
    #raw_cap.seek(0)
    frame_cnt = frame_cnt + 1
    #if the picam has captured 10 seconds of video leave the loop and stop recording
    if(frame_cnt> 100):
    	#cam.stop_preview()
    	#cam.close()
    	break
###################################################################################################################
    
print "Ending...."

GPIO.cleanup()    
cv2.destroyAllWindows()

