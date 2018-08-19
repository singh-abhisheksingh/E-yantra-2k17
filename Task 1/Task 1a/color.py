import cv2
import numpy as np 

img = cv2.imread('test images/trapezium.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,127,255,1)

_,contours,h = cv2.findContours(thresh,1,2)

for cnt in contours:
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    print cx,",",cy

colour = img[cy, cx]
print colour


if(colour[0]==0 and colour[1]==0 and colour[2]==255):
    print 'red'
else:
    print 'none'
    
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
