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
import numpy as np
from PIL import Image

from pprint import pprint
from os.path import expanduser

from train_faces_detect_face_5 import detect


import threading

#Initialize a face cascade using the frontal face haar cascade provided with
#the OpenCV library
faceCascade = cv2.CascadeClassifier('C:/Users/garvit/AppData/Local/conda/conda/envs/opencv-env/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

#The deisred output width and height
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600

PERSON_NAME = "Identifying person..."
IMAGE_URL = ""
trackingFace = False

def readImage():
    h = 648
    w = 1096

    # h = 720
    # w = 1280

    file = open('G:/rgbFrame.bin', 'r+')
    x = np.fromfile(file, dtype='uint8')

    if x.shape[0] != h*w*3:
        return (0, False)

    imageArray = x.reshape((h,w,3))

    imageArray = np.flip(imageArray, axis=1)
    imageArray = np.flip(imageArray, axis=2)

    # im = Image.fromarray(imageArray)
    file.close()
    return (imageArray, True)
    
def writeImage(image):
    image = np.flip(image, axis=1)
    image = np.flip(image, axis=2)
    image = image.reshape(image.shape[0] * image.shape[1] * image.shape[2])
    output_file = open('G:/rgbFrameRendered.bin', 'wb')
    # image.tofile(output_file)
    # output_file.close()

    newFileByteArray = bytearray(image)
    output_file.write(newFileByteArray)
    output_file.close()

def getName():
    global PERSON_NAME, trackingFace

    print("---> Reaching out to Azure to identify person...")
    # print("Calling detect with", IMAGE_URL)
    
    try:
        name, confidence = detect(IMAGE_URL)
        PERSON_NAME = str(name) + " (" + str(confidence) + ")"
    except:
        PERSON_NAME = "Identifying person..."
        global trackingFace
        trackingFace = False

def detectAndTrackLargestFace():
    #Open the first webcame device
    # capture = cv2.VideoCapture(0)

    #Create two opencv named windows
    
    #Position the windows next to eachother
    
    #Start the window thread for the two windows we are using
    
    #Create the tracker we will use
    tracker = dlib.correlation_tracker()

    #The variable we use to keep track of the fact whether we are
    #currently using the dlib tracker
    global trackingFace
    trackingFace = False

    #The color of the rectangle we draw around the face
    rectangleColor = (0,165,255)


    try:
        while True:
            #Retrieve the latest image from the webcam
            # rc,fullSizeBaseImage = capture.read()

            #Resize the image to 320x240
            # baseImage = cv2.resize( fullSizeBaseImage, ( 320, 240))
            # baseImage = fullSizeBaseImage
            fullBaseImage, truth = readImage()

            if truth == False:
                print("Fault -- fiber.exe sent a corrupted frame")
                continue
            else:
                baseImage = cv2.resize(fullBaseImage, (1096, 648))


            #Check if a key was pressed and if it was Q, then destroy all
            #opencv windows and exit the application
            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('q'):
                cv2.destroyAllWindows()
                exit(0)



            #Result image is the image we will show the user, which is a
            #combination of the original image from the webcam and the
            #overlayed rectangle for the largest face
            resultImage = baseImage.copy()






            #If we are not tracking a face, then try to detect one
            global trackingFace
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
                    cv2.imwrite("face-temp.jpg", face_image)
                    IMAGE_URL = "face-temp.jpg"

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
                if trackingQuality >= 6.75:
                    tracked_position =  tracker.get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    cv2.rectangle(resultImage, (t_x, t_y),
                                                (t_x + t_w , t_y + t_h),
                                                rectangleColor ,2)

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(resultImage, PERSON_NAME,(t_x, t_y + t_h + 28), font, 1,(255,255,255),1,cv2.LINE_AA)

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
            writeImage(largeResult)
            




    #To ensure we can also deal with the user pressing Ctrl-C in the console
    #we have to check for the KeyboardInterrupt exception and destroy
    #all opencv windows and exit the application
    except KeyboardInterrupt as e:
    	print("Detected Ctrl + C")
        cv2.destroyAllWindows()
        exit(0)


if __name__ == '__main__':
    detectAndTrackLargestFace()
