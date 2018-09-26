import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import time

##############################################################################################################
import motorMovement
import colorShape
import plantationOverlay
    
##############################################################################################################
counter = 0

def camcorder():
    contour_area = 0
    max_area = 0
    contour_index = 0
    contour = 0
    i = 0
    prev_area = 0
    flag = 1
    pastime = time.time()
    number = 0
    
    cam = PiCamera()
    cam.resolution = (320,240)
    cam.framerate = 60
    raw_cap = PiRGBArray(cam,(320,240))
    #frame_cnt = 0
    sleep(2.0)
    for frame in cam.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(320,240)):
        #image = frame.next()
        #extract opencv bgr array of color frame
        color_image = frame.array
        defectiveImage = color_image.copy()
        
        cv2.imshow("pi cam",color_image)
        #cv2.waitKey(1)
        #cv2.imshow('image',color_image)  
        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(17,17),0)
        
        #outGaussian.write(gray)
        #out.write(color_image)
                
        #gray = cv2.medianBlur(gray,7)
        #outMedian.write(gray)
        #cv2.imshow("Gaussian Blur",gray)
        
        img = color_image.copy()
        ret,thresh = cv2.threshold(gray,60,255,1)
        
        #cv2.imshow("gaussian thresh",thresh)
        #outThresh.write(thresh)
        #ret,thresh = cv2.threshold(gray,145,255,cv2.THRESH_BINARY)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        #dilation = cv2.dilate(thresh, kernel, iterations = 3)
        #erosion = cv2.erode(thresh, kernel, iterations = 3)
        #closing = cv2.erode(dilation, kernel, iterations = 3)
        #opening = cv2.dilate(erosion, kernel, iterations = 3)
        #painting = cv2.inpaint(img,dilation,3,cv2.INPAINT_TELEA)
        #paintedgray = cv2.cvtColor(painting, cv2.COLOR_BGR2GRAY)
        
        #ret,thresh = cv2.threshold(paintedgray,60,255,1)
        #cv2.imshow("before painting",gray)
        #cv2.imshow("painted gray",paintedgray)
        
        _,contours,h = cv2.findContours(thresh,1,2)
        #sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:7]
        
        i = 0
        max_area = 0

        if(contours):
        
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

            #print cx,",",cy
#####################################################################################################################
        
            #centroid = "("+str(cx) + "," + str(cy)+")"
            #cv2.putText(img, centroid, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            #cv2.putText(img, "centroid", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            #cv2.circle(img, (cx, cy), 4, (0,0,255), -1)
            
            height, width  = img.shape[:2]
            height = height/2
            width = width/2

            complete_area = height * width
            area_diff = prev_area - max_area
            prev_area = max_area
            #print area_diff
        
            #centre = "("+str(width) + "," + str(height)+")"
            #cv2.putText(img, centre, (width, height), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
            #cv2.putText(img, "centre", (width+20, height+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
#####################################################################################################################

            diff = cx - width
            #print diff
            difference = str(diff)
            cv2.putText(img, difference, (width + diff + 10,height + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
            cv2.circle(img, (width + diff,height), 4, (0,0,255), -1)
            cv2.circle(img, (width, height), 4, (255,0,0), -1)
            
            #cv2.drawContours(img,contours,contour_index,(0,255,0),3)
            #cv2.imshow('contour',thresh)
#####################################################################################################################

            global counter
            global hsv
            #hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            colour = colorShape.col(color_image)
            
            '''
            if flag == 0 :
                if ((time.time() - pastime) > 3):
                    flag = 1
                    pastime = time.time()
                    number = 0
            '''        
            
            if 1 :
            #(area_diff>5000) and colour and flag:
                flag = 0
                #motorMovement.left.stop()
                #motorMovement.right.stop()
                #hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                #gray = cv2.GaussianBlur(img,(5,5),0)
                #gray = cv2.medianBlur(gray,7)
                
                ret1, thresh1 = cv2.threshold(gray,80,255,1)
                erosion = cv2.erode(thresh1, kernel, iterations = 3)
                #cv2.imshow("Erosion",erosion)
                #outEroded.write(erosion)
                _,contours1,h = cv2.findContours(erosion,cv2.RETR_EXTERNAL,2)
                sorted_contours1 = sorted(contours1, key=cv2.contourArea, reverse=True)[:2]
                '''
                colorShape.tri = 0
                colorShape.sq = 0
                colorShape.cir = 0
                '''
                del sorted_contours1[0]
                #cv2.imshow('eroded image',erosion)
                print "yuhu"
                print sorted_contours1   
                #shape = colorShape.shap(sorted_contours1[1])
                
                #edges = cv2.Canny(color_image,100,200)
                #cv2.imwrite('canny.png',edges)
                #j = 0
                for cnt1 in sorted_contours1:
                    '''
                    if j == 0:
                      j = j+1
                      continue
                  ` '''
                    cv2.drawContours(img,cnt1,-1,(0,255,0),3)
                    
                    #x1,y1,w1,h1 = cv2.boundingRect(sorted_contours1[1])
                    #cv2.drawContours(defectiveImage,(x1,y1),(x1+w1,y1+h1),(0,0,255),0)
                    hull = cv2.convexHull(cnt1)
                    cv2.drawContours(defectiveImage,[hull],-1,(0,0,255),3)
                    
                    hull = cv2.convexHull(cnt1,returnPoints = False)
                    defects = cv2.convexityDefects(cnt1,hull)
                    
                    for i in xrange(defects.shape[0]):
                        st,en,fr,dist = defects[i,0]
                        start = tuple(cnt1[st][0])
                        end = tuple(cnt1[en][0])
                        far = tuple(cnt1[fr][0])
                        cv2.circle(defectiveImage,far,5,[255,0,0],-1)
                        cv2.line(defectiveImage,far,end,[255,255,0],2)
                        cv2.line(defectiveImage,start,far,[255,255,0],2)
                        
                cv2.imshow("Image",img)        
                cv2.imshow("defects",defectiveImage)
                
                    #outContours.write(img)
                '''
                    shape_area = cv2.contourArea(cnt1)
                    
                    M = cv2.moments(cnt1)
                    if(M['m00'] == 0):
                        M['m00'] = 1
                    cx1 = int(M['m10']/M['m00'])
                    cy1 = int(M['m01']/M['m00'])
                    diff1 = abs(cx1 - cx)
                    #print diff1
                    if diff1 > 50 and diff1 < 105 :
                        number = number + 1        
                    #print shape_area
                    j = j+1
                    #if (cv2.contourArea(cnt1) == max_area):
                        #continue
                    #shape = colorShape.shap(cnt1)
                
                cv2.imwrite("color.png",img)
                cv2.imwrite("eroded.png",erosion)
                print "NUMBER: ",number
                #print shape
                #motorMovement.left.stop()
                #motorMovement.right.stop()
                
                if (colorShape.cir):
                    print "CIRCLES: ",colorShape.cir
                if (colorShape.sq):
                    print "SQUARES: ",colorShape.sq
                if (colorShape.tr):
                    print "TRIANGLES: ",colorShape.tr
                '''
                #sleep(4)
                #colour = colorShape.col(color_image)
                #for cnt1 in contours1:
                    #shape = colorShape.shap(cnt1)
                    #colour = colorShape.col(hsv)

                    #plantationOverlay.overlay(colour, shape, counter)
                    #z1,z2,z3,z4 values reset after every call
                    
                counter = counter + 1
        '''  
            if(diff > 40):
                motorMovement.right_call()

            elif(diff < -40):
                motorMovement.left_call()

            else:
                motorMovement.forward_call()

                    
            if cv2.waitKey(1) == 27:
                break

        else:
            print "NO CONTOURS FOUND"
            motorMovement.backward_call()
        '''
######################################################################################################################

        raw_cap.truncate(0)
        raw_cap.seek(0)
#######################################################################################################################
    print counter
    
    print "Ending...."
    
    GPIO.cleanup()    
    cv2.destroyAllWindows()

def main():
    camcorder()
    
if __name__ == "__main__":
    main()
