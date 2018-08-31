import numpy as np
import cv2

cap = cv2.VideoCapture('VID3.mp4')

contour_area = 0
max_area = 0
contour_index = 0
contour = 0
i = 0

while(1):
    ret, frame = cap.read()
    
    #for k in range(0,5):
    #    ret, frame = cap.read()
        #cap.grab()
    
    #frame = cv2.imread('path.png')
    img = frame.copy()
    cv2.imshow('input',frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

    diff = cx - width
    difference = str(diff)
    cv2.putText(img, difference, (width + diff + 10,height + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    cv2.circle(img, (width + diff,height), 4, (0,0,255), -1)
    cv2.circle(img, (width, height), 4, (255,0,0), -1)
    
    cv2.drawContours(img,contours,contour_index,(0,255,0),3)
    cv2.imshow('contour',img)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

