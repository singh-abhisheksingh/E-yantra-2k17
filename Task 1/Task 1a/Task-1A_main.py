#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results1A_1776.csv'
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
    filep.close()

def main(path):
#####################################################################################################
    #Write your code here!!!
    img = cv2.imread(path)                          #taking the image through its path(work image) and storing it on variable 'img'
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    #converting the work image in its gray scale and storing it in variable gray
    r=[]                                            #variable 'r' defines a List used to display the complete information af all the shapes in an image.
    im_name=os.path.basename(path)
    r.append(im_name)                               # this statement stores the particular shape found in the image to List 'r'
    col=""                                          #variable to store colour of the particular shapes found in the image
    shape=""                                        #variable to store shape of the particular shapes found in the image

    ret,thresh = cv2.threshold(gray,127,255,1)      #thrsholding the image to use to find countours
    _,contours,h = cv2.findContours(thresh,1,2)     #finding the countours of the image and storing it in variable 'countours' 

    for cnt in contours:                            #variable cnt denotes the elements of the List 'contours'
        t=[]                                        
        M = cv2.moments(cnt)                        
        cx = int(M['m10']/M['m00'])                 #finding the centroid of the detected countours
        cy = int(M['m01']/M['m00'])                 

        centroid = "("+str(cx) + "," + str(cy)+")"  #variable to store the centroid
        cv2.putText(img, centroid, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)#function to write the centroid on the required shape
        
        colour = img[cy, cx]                                                              #variable to store the centroid pixel of the the detected shape 

        if(colour[0]>=0 and colour[0]<=10 and colour[1]>=0 and colour[1]<=10 and colour[2]>=245 and colour[2]<=255):    #checking for the red colour of the shape 
            col='red'
            cv2.putText(img, "red", (cx-20, cy-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)  #displays the colour in the upper left of the centroid
        elif(colour[0]<=255 and colour[0]>=245 and colour[1]>=0 and colour[1]<=10 and colour[2]>=0 and colour[2]<=10):  #checking for the blue colour of the shape
            col='blue'
            cv2.putText(img, "blue", (cx-20, cy-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1) #displays the colour in the upper left of the centroid
        elif(colour[0]>=0 and colour[0]<=10 and colour[1]>=121 and colour[1]<=134 and colour[2]>=0 and colour[2]<=10):  #checking for the green colour of the shape
            col='green'
            cv2.putText(img, "green", (cx-20, cy-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)#displays the colour in the upper left of the centroid

        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)                  #function to detect the approx shape and store it in variable 'approx' 
        if len(approx)==5:                                                                #checking for number of sides in a shape
            shape="pentagon"
            cv2.putText(img, "pentagon", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)#displaying the shape on the lower right corner of the centroid
        elif len(approx)==3:
            shape="triangle"
            cv2.putText(img, "triangle", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)
        elif len(approx)==4:
            (x, y, w, h) = cv2.boundingRect(approx)                                          #stores the x,y cordinates, widht and height of the rectangle bounding shape
            ar = w / float(h)                                                                #finding out the aspect ratio to clear out the confusion between trapezium and rhombus
            
            if ar>=1.8 :                                                                     #condition to check the aspect ratio of trapezium
                shape="trapezium"
                cv2.putText(img, "trapezium", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)
            else:
                shape="rhombus"
                cv2.putText(img, "rhombus", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)#displaying the shape on the lower right corner of the centroid
        elif len(approx) > 15:                                                                  #condition to check if the shape is circle
            shape="circle"
            cv2.putText(img, "circle", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)     #displaying the shape on the lower right corner of the centroid
        elif len(approx) == 6:                                                                  #checking for number of sides in a shape
            shape="hexagon"
            cv2.putText(img, "hexagon", (cx+20, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 1)    #displaying the shape on the lower right corner of the centroid
        t.append(str(col+'-'+shape+'-'+str(cx)+'-'+str(cy)))                                    #this statement stores the "colour,shape and centoid" of a particular shape as a list 't'
        r.append(t)                                                                             #this statement stores the list 't' in List 'r'
        writecsv(col,shape,(cx,cy))                                                             #function to write as CSV file
    cv2.imwrite(im_name[ :-4]+'output.png',img)                   
    return r       
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    global filename
    mypath = 'E:/eyantra 2017/task1_pb_set11/Set 11/Task 1/Task1A/2. Task_Description/Test Images'
    #getting all files in the directory
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open(filename,'a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open(filename,'a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
