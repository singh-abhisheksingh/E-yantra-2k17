import cv2
import numpy as np
import os

z1 = 0
z2 = 0
z3 = 0
z4 = 0
plantation = cv2.imread("Plantation\\Plantation.png",-1)

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

def overlay(col, sha, det):

    global z1
    global z2
    global z3
    global z4
    
    zone1 = [(100,190),(135,190),(50,220),(85,220)]
    zone2 = [(225,160),(260,160),(295,160),(330,160)]
    zone3 = [(330,230),(365,230),(400,230),(435,230)]
    zone4 = [(530,170),(565,170),(600,170),(635,170)]

    assorted = cv2.imread("Seedlings\\assorted.png",-1)
    carnation = cv2.imread("Seedlings\\carnation.png",-1)
    gerber = cv2.imread("Seedlings\\gerber.png",-1)
    hibiscusred = cv2.imread("Seedlings\\hibiscusred.png",-1)
    hibiscusyellow = cv2.imread("Seedlings\\hibiscusyellow.png",-1)
    hydrangeablue = cv2.imread("Seedlings\\hydrangeablue.png",-1)
    hydrangeayellow = cv2.imread("Seedlings\\hydrangeayellow.png",-1)
    lilac = cv2.imread("Seedlings\\lilac.png",-1)
    lily = cv2.imread("Seedlings\\lily.png",-1)
    marigold = cv2.imread("Seedlings\\marigold.png",-1)
    morningglory = cv2.imread("Seedlings\\morningglory.png",-1)
    orchid = cv2.imread("Seedlings\\orchid.png",-1)
    poinsettia = cv2.imread("Seedlings\\poinsettia.png",-1)
    rosered = cv2.imread("Seedlings\\rosered.png",-1)
    roseyellow = cv2.imread("Seedlings\\roseyello.png",-1)
    sunflower = cv2.imread("Seedlings\\sunflower.png",-1)
    tulipblue = cv2.imread("Seedlings\\tulipblue.png",-1)
    tulipred = cv2.imread("Seedlings\\tulipred.png",-1)

    color = col
    shape = sha
    detectedZone = det

    if(color == "red"):
        if(shape == "square"):
            image = rosered
        elif(shape == "circle"):
            image = gerber
        elif(shape == "triangle"):
            image = poinsettia
    elif(color == "blue"):
        if(shape == "square"):
            image = orchid
        elif(shape == "circle"):
            image = tulipblue
        elif(shape == "triangle"):
            image = lilac
    elif(color == "green"):
        if(shape == "square"):
            image = hibiscusyellow
        elif(shape == "circle"):
            image = lily
        elif(shape == "triangle"):
            image = marigold
    
    #resizing the image to be overlaid
    overlay_image = cv2.resize(image,(30,40))
    
    if(detectedZone == "1"):
        x = zone1[z1][0]
        y = zone1[z1][1]
        z1 = z1 + 1
    elif(detectedZone == "2"):
        x = zone2[z2][0]
        y = zone2[z2][1]
        z2 = z2 + 1
    elif(detectedZone == "3"):
        x = zone3[z3][0]
        y = zone3[z3][1]
        z3 = z3 + 1
    elif(detectedZone == "4"):
        x = zone4[z4][0]
        y = zone4[z4][1]
        z4 = z4 + 1

    print x,",",y
    
    #overlaying the seedlings
    plantation[y:y+40,x:x+30,:] = blend_transparent(plantation[y:y+40,x:x+30,:], overlay_image)   #passing the overlaying image to the function
    cv2.imwrite("Overlayed_Plantation.jpg", plantation)
    #cv2.imshow("Overlayed_Plantation.jpg", plantation)

    cv2.destroyAllWindows()      

def main():
    overlay("blue","circle","1")
    overlay("blue","triangle","2")
    overlay("red","circle","3")
    overlay("red","triangle","4")
    overlay("green","circle","4")
    overlay("green","square","2")
    
if __name__ == "__main__":
    main()
