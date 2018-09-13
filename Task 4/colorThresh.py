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
    imageb = color_image.copy()
    imageg = color_image.copy()
    imager = color_image.copy()
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    
    #gray = cv2.medianBlur(gray,9)

    #gray = cv2.bilateralFilter(gray,6,75,75)
          
    ret,thresh = cv2.threshold(gray,145,255,cv2.THRESH_BINARY)

    #rety,threshy = cv2.threshold(gray,60,255,cv2.THRESH_BINARY_INV)
    
    #cv2.imwrite("threshy.png",threshy)
    #thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,21,8)
    #thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,21,8)
    
    #gray = cv2.GaussianBlur(gray,(5,5),0)
    
    #ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    #thresh = fgbg.apply(gray)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    dilation = cv2.dilate(thresh, kernel, iterations = 1)
    #closing = cv2.erode(dilation, kernel, iterations = 3)
    
    painting = cv2.inpaint(img,dilation,3,cv2.INPAINT_TELEA)
    
    
    '''
    #imageb[:,:,0]=0 #Blue channel of image
    imageb[:,:,1]=0 #Green channel of image
    imageb[:,:,2]=0 #Red channel of image

    grayb = cv2.cvtColor(imageb, cv2.COLOR_BGR2GRAY)
    retb, threshb = cv2.threshold(grayb,20,255,cv2.THRESH_BINARY)
    
    bdilation = cv2.dilate(threshb, kernel, iterations = 1)
    paintb = cv2.inpaint(img,bdilation,3,cv2.INPAINT_TELEA)
    
    #cv2.imshow("channel",image)
    #cv2.imshow("grayb",grayb)
    #cv2.imshow("channel blue",bdilation)
    
    
    imageg[:,:,0]=0 #Blue channel of image
    #imageg[:,:,1]=0 #Green channel of image
    imageg[:,:,2]=0 #Red channel of image

    grayg = cv2.cvtColor(imageg, cv2.COLOR_BGR2GRAY)
    retg, threshg = cv2.threshold(grayg,80,255,cv2.THRESH_BINARY)
    
    gdilation = cv2.dilate(threshg, kernel, iterations = 1)
    paintg = cv2.inpaint(img,gdilation,3,cv2.INPAINT_TELEA)
    
    #cv2.imshow("channel",image)
    #cv2.imshow("grayg",grayg)
    #cv2.imshow("channel green",gdilation)
    
    
    imager[:,:,0]=0 #Blue channel of image
    imager[:,:,1]=0 #Green channel of image
    #imager[:,:,2]=0 #Red channel of image

    grayr = cv2.cvtColor(imager, cv2.COLOR_BGR2GRAY)
    retr, threshr = cv2.threshold(grayr,40,255,cv2.THRESH_BINARY)
    
    rdilation = cv2.dilate(threshr, kernel, iterations = 1)
    paintred = cv2.inpaint(img,rdilation,3,cv2.INPAINT_TELEA)
    
    #cv2.imshow("channel",image)
    #cv2.imshow("grayb",grayb)
    #cv2.imshow("channel red",rdilation)
    '''
    
    paintedgray = cv2.cvtColor(painting, cv2.COLOR_BGR2GRAY)
    rety,threshy = cv2.threshold(paintedgray,60,255,cv2.THRESH_BINARY_INV)
    
    equ = cv2.equalizeHist(gray)
    #res = np.hstack((gray,equ)) #stacking images side-by-side
    #rethist,threshist = cv2.threshold(equ,80,255,cv2.THRESH_BINARY)
    
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(16,16))
    cl1 = clahe.apply(gray)
    rethist,threshist = cv2.threshold(cl1,60,255,cv2.THRESH_BINARY_INV)
    
    _,contours,h = cv2.findContours(threshy,1,2)
    
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
    cv2.drawContours(painting,contours,contour_index,(0,255,0),3)
    
    #cv2.imshow('gray',gray)
    #cv2.imshow('contour',img)
    #cv2.imshow('thresh',thresh)
    cv2.imshow('threshy',threshy)
    #cv2.imshow('dilation',dilation)
    #cv2.imshow('painting',painting)
    #cv2.imshow('histogram',equ)
    cv2.imshow('threshed histogram',threshist)
    #cv2.imshow('clahe',cl1)


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
    #if(frame_cnt> 100):
    	#cam.stop_preview()
    	#cam.close()
    	#break

print "Ending...."

cv2.destroyAllWindows()

