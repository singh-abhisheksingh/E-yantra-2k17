import numpy as np
import cv2

img = cv2.imread('trapezium.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,127,255,1)

_,contours,h = cv2.findContours(thresh,1,2)

for cnt in contours:
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    print cx,",",cy
    
    centroid = "("+str(cx) + "," + str(cy)+")"
    cv2.putText(img, centroid, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)
    cv2.putText(img, "centroid", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)


cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
