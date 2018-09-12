import numpy as np
import cv2

cap = cv2.VideoCapture('VID.mp4')

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('Output.avi',fourcc, 16.0, (640,480))

contour_area = 0
max_area = 0
contour_index = 0
i = 0
#(cap.isOpened())
while(1):
    ret, frame = cap.read()

    for k in range(0,5):
        ret, frame = cap.read()
        #cap.grab()
    
    #frame = cv2.imread('pa.png')
    img = frame.copy()
    cv2.imshow('input',frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    ret,thresh = cv2.threshold(gray,127,255,1)
    #cv2.imshow('thresh',thresh)
    _,contours,h = cv2.findContours(thresh,1,2)
    #cv2.drawContours(img,contours,-1,(0,255,0),3)
    #cv2.imshow('contour',img)

    i = 0
    max_area = 0
    for cnt in contours:
        contour_area = cv2.contourArea(cnt)
        if(max_area < contour_area):
            max_area = contour_area
            contour_index = i
        i = i+1

        tilted = cv2.minAreaRect(cnt)
        rect = cv2.boxPoints(tilted)
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        print("START")
        print(rect)
        print("LOL")
        print(approx)
        rect = np.int0(rect)
        approx = np.int0(approx)
        #x,y,w,h = cv2.boundingRect(cnt)
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
        #cv2.drawContours(img,[rect],-1,(255,0,0),3)
        #cv2.drawContours(img,[approx],-1,(0,0,255),3)
    cv2.drawContours(img,contours,contour_index,(0,255,0),3)
    cv2.imshow('contour',img)
        
    if cv2.waitKey(1) == 27:
        break

cap.release()
#out.release()
cv2.destroyAllWindows()
