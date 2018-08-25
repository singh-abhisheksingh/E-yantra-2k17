#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results1B_1776.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


def main(video_file_with_path):
    cap = cv2.VideoCapture(video_file_with_path)
    image_red = cv2.imread("Overlay_Images\\yellow_flower.png",-1)
    image_blue = cv2.imread("Overlay_Images\\pink_flower.png",-1)
    image_green = cv2.imread("Overlay_Images\\red_flower.png",-1)

#####################################################################################################
    #Write your code here!!!

    fourcc = cv2.VideoWriter_fourcc(*'XVID')						
    out = cv2.VideoWriter('Videooutput.mp4',fourcc, 16.0,(1280,720))
    list1=[]                                                        #it is a List of centroid
    list2=[]                                                        #List of shapes
    col=[]                                                          #List of colours
    x=0                                                             #x coordinate of bounding rect
    y=0                                                             #y coordinate of bounding rect
    w=0                                                             #width of the bounding rect
    h=0                                                             #height of the bounding rect
    j=0                                                             #it is used to access the centroid of the shape of previous frame
    flag=0                                                          #it is used to check the condition for overlaying(if flag =1,then overlay will be done)
    '''  "flagPost" and "newFlag" have been
         defined to overcome the flickering
         problem in the shapes of the video
    '''
    flagPost=0                                                      #it is used to ignore the new frame if it is found same as the previous frame
    newFlag=0                                                       #it is used to check whether the new frame is near to the previous frame
    image = image_red                                               #to store image which needs to be overlaid
    while True:
        ret,frame = cap.read()                                      #to capture each frame and store in 'frame'
        if ret==True:                                               #to check if we are getting any frame or not
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
            ret,thresh = cv2.threshold(gray,127,255,1)
            _,contours,_ = cv2.findContours(thresh,1,2)             #to find the countours of the shapes in the video
            for cnt in contours:
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])                         #x coordinate of centroid
                cy = int(M['m01']/M['m00'])                         #y coordinate of centroid
                
                if(cx,cy) not in list1:                             #if this centroid is not in list then overlaying at this centroid will be done

                    if len(approx)==5:
                        list2.append("pentagon")
                    elif len(approx)==3:
                        list2.append("triangle")
                    elif len(approx)==4:
                        (x, y, w, h) = cv2.boundingRect(approx)
                        ar = w / float(h)                           #finding out the aspect ratio to clear out the confusion between trapezium and rhombus
                        
                        if ar>=1.8 :                                #condition to check the aspect ratio of trapezium
                            list2.append("trapezium")
                        else:
                            list2.append("rhombus")
                    elif len(approx) > 12:                          #condition to check the circle
                        list2.append("circle")
                    elif len(approx) == 6:                          #condition to check the circle
                        list2.append("hexagon")
                        
                    list1.append((cx,cy))                           #storing the centroid in list1
                    if newFlag>=2:
                        j = len(list1)-2
                        k = list1[j]                                #accesing the x,y coordinates in list1
                        if k[0]>=cx-80 and k[0]<=cx+80 and k[1]>=cy-80 and k[1]<=cy+80:     #checking whether the centroid of new frame is near the old frame 
                            flagPost=1
                    newFlag=newFlag+1
                    if flagPost==1:
                        list1.remove((k[0],k[1]))
                        list2.pop()
                        col.pop()
                        flagPost=0
                    colour = frame[cy, cx]                          #storing the colour of centroid
                    if(colour[0]>=0 and colour[0]<=10 and colour[1]>=0 and colour[1]<=10 and colour[2]>=245 and colour[2]<=255):
                        image = image_red
                        col.append('Red')
                    elif(colour[0]<=255 and colour[0]>=245 and colour[1]>=0 and colour[1]<=10 and colour[2]>=0 and colour[2]<=10):
                        image = image_blue
                        col.append('Blue')
                    elif(colour[0]>=0 and colour[0]<=10 and colour[1]>=121 and colour[1]<=134 and colour[2]>=0 and colour[2]<=10):
                        image = image_green
                        col.append('Green')
                
                    (x, y, w, h) = cv2.boundingRect(approx)
                    flag=1
                    break
                
            if flag==1:
                overlay_image = cv2.resize(image,(w,h))             #resizing the image to be overlaid
                frame[y:y+h,x:x+w,:] = blend_transparent(frame[y:y+h,x:x+w,:], overlay_image)   #passing the overlaying image to the function
                    
            out.write(frame)
            cv2.waitKey(40)
        else:
            for p,q,r in zip(col,list2,list1):                      #passing the value to write csv
                writecsv(p,q,r)
            
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            break
#####################################################################################################

#####################################################################################################
    #sample of overlay code for each frame
    #x,y,w,h = cv2.boundingRect(current_contour)
    #overlay_image = cv2.resize(image_red,(h,w))
    #frame[y:y+w,x:x+h,:] = blend_transparent(frame[y:y+w,x:x+h,:], overlay_image)
#######################################################################################################

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main("Video.mp4")
