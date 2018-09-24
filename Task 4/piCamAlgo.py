import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
from time import sleep

contour_area = 0
max_area = 0
contour_index = 0
contour = 0
i = 0
###############################################################################################################

cam = PiCamera()
cam.resolution = (320,240)
cam.framerate = 60
raw_cap = PiRGBArray(cam,(320,240))
frame_cnt = 0
for frame in cam.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(320,240)):
    #time.sleep(1.0)
    #image = frame.next()
    #extract opencv bgr array of color frame
    color_image = frame.array
    #cv2.imshow("Input Video",color_image)
    #cv2.waitKey(1)
################################################################################################################

    img = color_image.copy()
    #canny_img = color_image.copy()
    
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,55,255,1)
    
    #ret,thresh = cv2.threshold(gray,145,255,cv2.THRESH_BINARY)
        
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    #dilation = cv2.dilate(thresh, kernel, iterations = 1)
    #closing = cv2.erode(dilation, kernel, iterations = 3)
    #painting = cv2.inpaint(img,dilation,3,cv2.INPAINT_TELEA)
    #paintedgray = cv2.cvtColor(painting, cv2.COLOR_BGR2GRAY)
    
    #ret,thresh = cv2.threshold(paintedgray,55,255,1)
    #cv2.imshow("before painting",gray)
    #cv2.imshow("painted gray",paintedgray)
    
    
    #thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,8)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    #thresh = fgbg.apply(gray)

    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    #dilation = cv2.dilate(thresh, kernel, iterations = 5)
    #closing = cv2.erode(dilation, kernel, iterations = 5)
    
    _,contours,h = cv2.findContours(thresh,1,2)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    
    i = 0
    max_area = 0
    
    for cnt in sorted_contours:
        if i == 0:
            i = i+1
            continue
        approx = cv2.approxPolyDP(cnt,0.08*cv2.arcLength(cnt,True),True)
        #cv2.drawContours(img,sorted_contours,i,(0,255,0),3)
        print approx
        print "new approx \n"
        sleep(5)
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
    
    #cv2.drawContours(img,contours,contour_index,(0,255,0),3)
    cv2.imshow('contour',img)
    cv2.imshow('thresh',thresh)
    
    #edges = cv2.Canny(painting,60,200)
    #dilated_edges = cv2.dilate(edges, kernel, iterations = 1)
    #cv2.imshow('canny edges',dilated_edges)
    
    #_,canny_contours,h = cv2.findContours(dilated_edges,1,2)
    #sorted_canny_contours = sorted(canny_contours, key=cv2.contourArea, reverse=True)[:7]
    
    #l = 0
    #for canny_cnt in sorted_canny_contours:
        #cv2.drawContours(canny_img,sorted_canny_contours,l,(0,255,0),3)
        #l = l + 1
    
    #cv2.imshow('canny contours',canny_img)
                

    if(diff > 40):
        print diff
        #turn right
    elif(diff < -40):
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
    #if(frame_cnt> 100):
    	#cam.stop_preview()
    	#cam.close()
    	#break

print "Ending...."

cv2.destroyAllWindows()

