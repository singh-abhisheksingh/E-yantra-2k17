import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time

contour_area = 0
max_area = 0
contour_index = 0
contour = 0
i = 0
###############################################################################################################

cam = PiCamera()
cam.resolution = (224,160)
cam.framerate = 5
raw_cap = PiRGBArray(cam,(224,160))
frame_cnt = 0
for frame in cam.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(224,160)):
    #time.sleep(1.0)
    #image = frame.next()
    #extract opencv bgr array of color frame
    color_image = frame.array
    #cv2.imshow("Input Video",color_image)
    #cv2.waitKey(1)
################################################################################################################

    img = color_image.copy()
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,90,255,1)
    _,contours,h = cv2.findContours(thresh,1,2)
    
    i = 0
    max_area = 0
    
    for cnt in contours:
        
        contour_area = cv2.contourArea(cnt)
        if(max_area < contour_area):
            max_area = contour_area
            contour_index = i
            contour = cnt
        i = i+1

    M = cv2.moments(contour)
    if(M['m00'] == 0):
        M['m00'] = 1
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    print cx,",",cy
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
    difference = str(diff)
    cv2.putText(img, difference, (width + diff + 10,height + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    cv2.circle(img, (width + diff,height), 4, (0,0,255), -1)
    cv2.circle(img, (width, height), 4, (255,0,0), -1)
    
    cv2.drawContours(img,contours,contour_index,(0,255,0),3)
    cv2.imshow('contour',img)

    if(diff > 25):
        print diff
        #turn right
    elif(diff < -25):
        print diff
        #turn left
    else:
        print diff
        #move forward
            
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

print "Ending...."

cv2.destroyAllWindows()

