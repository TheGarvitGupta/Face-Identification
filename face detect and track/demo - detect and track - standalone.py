#!/usr/bin/python
'''
    Author: Guido Diepen <gdiepen@deloitte.nl>
'''

#Import the OpenCV and dlib libraries
import cv2
import dlib
import time
import sys

import json, urllib, requests, httplib, base64

from pprint import pprint
from os.path import expanduser

from train_faces_detect_face_5 import detect


import threading

#Initialize a face cascade using the frontal face haar cascade provided with
#the OpenCV library
faceCascade = cv2.CascadeClassifier('C:/Users/garvit/AppData/Local/conda/conda/envs/opencv-env/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

#The deisred output width and height

PERSON_NAME = "Identifying person..."
IMAGE_URL = ""
trackingFace = False

timeStamp = 0
frames = 0

def getName():
    global PERSON_NAME, trackingFace

    print("---> Reaching out to Azure to identify person...")
    print("Calling detect with", IMAGE_URL)
    
    try:
        global PERSON_NAME, trackingFace

        name, confidence_float = detect(IMAGE_URL)
        confidence = float(confidence_float*100)

        if (confidence >= 80):
            confidence = "Very high confidence (" + str(round(confidence, 2)) + "%)"

        elif (confidence >= 70):
            confidence = "High confidence (" + str(round(confidence, 2)) + "%)"

        elif (confidence >= 50):
            confidence = "Moderate confidence (" + str(round(confidence, 2)) + "%)"

        else:
            confidence = "Low confidence (" + str(round(confidence, 2)) + "%)"

        if confidence_float < 0.4:
            name = "Face detected..."

        PERSON_NAME = str(name) + " -- " + confidence

    except Exception as e:
        print("Exception:" + str(e))
        
        global PERSON_NAME, trackingFace
        PERSON_NAME = "Identifying person..."
        trackingFace = False

def detectAndTrackLargestFace():
    #Open the first webcame device
    capture = cv2.VideoCapture(0)
    capture.set(3,1280)
    capture.set(4,720)

    #Create two opencv named windows
    # cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)

    #Position the windows next to eachother
    cv2.moveWindow("result-image",50,50)

    #Start the window thread for the two windows we are using
    cv2.startWindowThread()

    #Create the tracker we will use
    tracker = dlib.correlation_tracker()

    #The variable we use to keep track of the fact whether we are
    #currently using the dlib tracker
    global trackingFace
    trackingFace = False

    #The color of the rectangle we draw around the face
    themeColor = (161,71,13)

    d_t_x = 0
    d_t_y = 0

    d_t_w = 0
    d_t_h = 0

    # Thresholds to stabilize overlay flicker
    rectangle_threshold = 15
    area_threshold = 15

    try:
        while True:

            # Frame rate

            global timeStamp, frames, trackingFace

            frames += 1
            if time.time() - timeStamp >= 1:
                frameRate = "FPS:" + str(frames)
                frames = 0
                timeStamp = time.time()

            #Retrieve the latest image from the webcam
            rc,fullSizeBaseImage = capture.read()

            #Resize the image to 320x240
            # baseImage = cv2.resize( fullSizeBaseImage, ( 320, 240))
            baseImage = fullSizeBaseImage


            #Check if a key was pressed and if it was Q, then destroy all
            #opencv windows and exit the application
            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('q'):
                cv2.destroyAllWindows()
                exit(0)

            elif pressedKey == ord('t') or pressedKey == ord('T'):
                trackingFace = False



            #Result image is the image we will show the user, which is a
            #combination of the original image from the webcam and the
            #overlayed rectangle for the largest face
            resultImage = baseImage.copy()

            cv2.putText(resultImage, frameRate,(10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, themeColor,1,cv2.LINE_AA)






            #If we are not tracking a face, then try to detect one
            if not trackingFace:

                #For the face detection, we need to make use of a gray
                #colored image so we will convert the baseImage to a
                #gray-based image
                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)

                #Now use the haar cascade detector to find all faces
                #in the image
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)

                #In the console we can show that only now we are
                #using the detector for a face
                print("Using the cascade detector to detect face")

                #For now, we are only interested in the 'largest'
                #face, and we determine this based on the largest
                #area of the found rectangle. First initialize the
                #required variables to 0
                maxArea = 0
                x = 0
                y = 0
                w = 0
                h = 0


                #Loop over all faces and check if the area for this
                #face is the largest so far
                #We need to convert it to int here because of the
                #requirement of the dlib tracker. If we omit the cast to
                #int here, you will get cast errors since the detector
                #returns numpy.int32 and the tracker requires an int
                for (_x,_y,_w,_h) in faces:
                    if  _w*_h > maxArea:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)
                        maxArea = w*h

                #If one or more faces are found, initialize the tracker
                #on the largest face in the picture
                if maxArea > 0 :

                    #Initialize the tracker
                    tracker.start_track(baseImage,
                                        dlib.rectangle( x-10,
                                                        y-20,
                                                        x+w+10,
                                                        y+h+20))

                    #Set the indicator variable such that we know the
                    #tracker is tracking a region in the image
                    global trackingFace
                    trackingFace = True
                    
                    global IMAGE_URL
                    global PERSON_NAME

                    PERSON_NAME = "Identifying person..."
                    print("Found a face")

                    face_image = baseImage[y-20:(y+h + 20), x-10:(x+w+10)]

                    random = "faces/" + str(time.time()) + ".jpg"

                    cv2.imwrite(random, face_image)
                    IMAGE_URL = random

                    print("Set", IMAGE_URL)
                    print("Calling getName")
                    threading.Thread(target=getName).start()

                else:
                    print("Could not track any faces")

            #Check if the tracker is actively tracking a region in the image

            if trackingFace:

                #Update the tracker and request information about the
                #quality of the tracking update
                trackingQuality = tracker.update( baseImage )



                #If the tracking quality is good enough, determine the
                #updated position of the tracked region and draw the
                #rectangle
                if trackingQuality >= 6:
                    tracked_position =  tracker.get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())

                    # Stabilize coordinate movement and area change

                    if (abs(d_t_x - t_x) + abs(d_t_y - t_y) > rectangle_threshold):
                        d_t_x = t_x
                        d_t_y = t_y

                    if (abs(d_t_h - t_h) + abs(d_t_w - t_w) > area_threshold):
                        d_t_h = t_h
                        d_t_w = t_w

                    cv2.rectangle(resultImage, (d_t_x, d_t_y),
                                                (d_t_x + d_t_w , d_t_y + d_t_h),
                                                themeColor ,2)

                    font = cv2.FONT_HERSHEY_SIMPLEX

                    if PERSON_NAME != "Identifying person...":
                        name, confidence = PERSON_NAME.split(" -- ")

                    else:
                        name = PERSON_NAME
                        confidence = ""

                    cv2.putText(resultImage, name,(d_t_x, d_t_y + d_t_h + 25), font, 0.8, themeColor,1,cv2.LINE_AA)
                    cv2.putText(resultImage, confidence,(d_t_x, d_t_y + d_t_h + 45), font, 0.5, themeColor,1,cv2.LINE_AA)

                else:
                    #If the quality of the tracking update is not
                    #sufficient (e.g. the tracked region moved out of the
                    #screen) we stop the tracking of the face and in the
                    #next loop we will find the largest face in the image
                    #again
                    global trackingFace
                    trackingFace = False





            #Since we want to show something larger on the screen than the
            #original 320x240, we resize the image again
            #
            #Note that it would also be possible to keep the large version
            #of the baseimage and make the result image a copy of this large
            #base image and use the scaling factor to draw the rectangle
            #at the right coordinates.
            # largeResult = cv2.resize(resultImage,
            #                          (OUTPUT_SIZE_WIDTH,OUTPUT_SIZE_HEIGHT))

            largeResult = resultImage

            #Finally, we want to show the images on the screen
            # cv2.imshow("base-image", baseImage)
            cv2.imshow("result-image", largeResult)




    #To ensure we can also deal with the user pressing Ctrl-C in the console
    #we have to check for the KeyboardInterrupt exception and destroy
    #all opencv windows and exit the application
    except KeyboardInterrupt as e:
        print("Detected Ctrl + C")
        cv2.destroyAllWindows()
        exit(0)


if __name__ == '__main__':
    detectAndTrackLargestFace()