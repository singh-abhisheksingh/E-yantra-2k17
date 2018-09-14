
############################################
## Import OpenCV
import numpy as np
import cv2
############################################

############################################
## Read the image
img= cv2.imread('sample.png')
print "original image matrix = ", img.shape
############################################

############################################
## Do the processing
############################################
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print "hsv image matrix = ", hsv.shape

(width, height, channel)= hsv.shape
hue = np.zeros((width,height), np.uint8)
saturation = np.zeros((width,height), np.uint8)
value = np.zeros((width,height), np.uint8)

hue = hsv[:, :, 0]
saturation = hsv[:, :, 1] + 50
value = hsv[:, :, 2]
############################################
## Show the image
cv2.imshow('image',img)
cv2.imshow('hue', hue)
cv2.imshow('saturation', saturation)
cv2.imshow('value', value)
############################################

############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
