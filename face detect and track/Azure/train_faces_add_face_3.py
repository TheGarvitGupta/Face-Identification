import httplib, urllib, base64, requests
from keys import SubscriptionKey
import os
import time
officePath = "C:/Users/garvit/Desktop/Extract Images/Mountain View - 520"
databasePath = "people_database/"
databaseName = "Mountain View - 520.txt"
personGroupId = "0"

def images(personName, officePath):
    # Returns list of absolute image paths for person name and office path (absolute)
    directory = officePath + "/" + personName
    images = os.walk(directory)
    images = [image for image in images][0][2]
    imageURLs = []
    for image in images:
        imageURLs.append(directory + '/' + image)
    return imageURLs

# name: All the keys -> name mapping
# identity: All the name -> keys mapping
file = open(databasePath + databaseName, 'r')
name = eval(file.read())
identity = {}
for key in name:
    identity[name[key]] = key
uploaded = 1
for person in identity:
    personImages = images(person, officePath)
    print ("Uploading [" + str(uploaded) + "/" + str(len(identity)) + str("]"))
    imagesUploaded = 1
    for imageURL in personImages:
        print (person + ": " + imageURL + " [" + str(imagesUploaded) + "/" + str(len(personImages)) + "]")
        # API limit: Up to 10 transactions per second
        time.sleep(0.1)
        # API Call
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': SubscriptionKey,
        }
        params = urllib.urlencode({
            'personGroupId': personGroupId,
            'personId': identity[person]
        })
        url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/' + personGroupId + '/persons/' + identity[person] + '/persistedFaces?%s' % params
        img = open(imageURL, 'rb')
        response = requests.post(url, data=img, headers=headers)
        print ("\t" + str(response.status_code) + "\t" + str(response.text))
        # Images uploaded
        imagesUploaded += 1
    # People uploaded
    uploaded += 1