import numpy as np
import cv2

cap = cv2.VideoCapture('Video.mp4')

while(1):
    #ret, frame = cap.read()
    frame = cv2.imread('path.png')
    img = frame.copy()
    cv2.imshow('input',frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,1)
    _,contours,h = cv2.findContours(thresh,1,2)
    for cnt in contours:
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        print cx,",",cy
        
        centroid = "("+str(cx) + "," + str(cy)+")"
        cv2.putText(img, centroid, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        cv2.putText(img, "centroid", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        height, width  = img.shape[:2]
        height = height/2
        width = width/2
        centre = "("+str(width) + "," + str(height)+")"
        cv2.putText(img, centre, (width, height), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
        cv2.putText(img, "centre", (width+20, height+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
        
    cv2.imshow('contour',img)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

