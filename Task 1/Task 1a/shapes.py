import numpy as np
import cv2

img = cv2.imread('test images/trap.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,127,255,1)

_,contours,h = cv2.findContours(thresh,1,2)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print len(approx)
    area_cnt = cv2.contourArea(cnt)
    if len(approx)==5:
        print "pentagon"
        cv2.drawContours(img,[cnt],0,255,-1)
    elif len(approx)==3:
        print "triangle"
        cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    elif len(approx)==4:
        (x, y, w, h) = cv2.boundingRect(approx)
        area_bound = w*h*1.0

        print area_cnt
        print area_bound
        
        ar = w / float(h)
        print ar
        if ar >= 0.95 and ar <= 1.05 :
            print "square"
        elif ar>=1.8 :
            print "trapezium"
        else:
            area = area_bound - area_cnt
            if area<=3000:
                print "rectangle"
            else: print "rhombus"
        cv2.drawContours(img,[cnt],0,(0,0,255),-1)
    elif len(approx) == 9:
        print "half-circle"
        cv2.drawContours(img,[cnt],0,(255,255,0),-1)
    elif len(approx) > 15:
        print "circle"
        cv2.drawContours(img,[cnt],0,(0,255,255),-1)
    elif len(approx) == 6:
        print "hexagon"
        cv2.drawContours(img,[cnt],0,(255,0,255),-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
