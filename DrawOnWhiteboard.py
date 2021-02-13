"""
Created on Sat 13 Feb 1:14:07 2021

@author: purvitsharma

"""
import cv2  #importing library for computervision
import numpy as np #importing numpy library
width = 640
height = 480
cap = cv2.VideoCapture(0)   #input from webcam(default)
cap.set(3, width)
cap.set(4, height)
cap.set(10,150) # brightness adjustment

mycolors = [[145, 135, 86, 168, 212, 185], #pink
            [0, 140, 125, 12, 209, 241], #orange
            [36, 60, 28, 102, 169, 141]  #green
            ]

mycolorvalues = [[153,102,255],                #BGR format
                 [26,140,255],
                 [51,204,51]
                 ]
mypoints = []           # [x,y,colorID]

def findcolor(img, mycolors,mycolorvalues):  #function to find colours and return points
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)   #converting original image
    count = 0                       #counter declared for different colours
    newpoints = []                  #empty list of newpoints

    for color in mycolors:                      #loop for different colours
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getcontours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorvalues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count +=1
        #cv2.imshow(str(color[0]),mask)
    return newpoints

def getcontours(img):           #returning contours
    x,y,w,h = 0,0,0,0
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >500 :
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y


def draw(mypoints,mycolorvalues):       #function to draw through colours specified in mycolors list
    for point in mypoints:
        cv2.circle(imgResult,(point[0],point[1]),6,mycolorvalues[point[2]],cv2.FILLED)

while True:
    success, img = cap.read()

    imgResult = img.copy()      #make copy of original image

    newpoints = findcolor(img, mycolors, mycolorvalues)     #getting newpoints

    if len(newpoints)!=0:
        for new in newpoints:
            mypoints.append(new)

    if len(mypoints)!=0:
        draw(mypoints,mycolorvalues)

    cv2.imshow("Whiteboard",imgResult)  # displaying window where we will draw

    if cv2.waitKey(1) & 0xFF == ord("q"):   # for quiting thw camera whiteboard window press q
        break
