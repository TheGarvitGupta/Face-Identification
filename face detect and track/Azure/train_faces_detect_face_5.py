import json, urllib, requests, httplib, base64

from pprint import pprint
import os
from os.path import expanduser
from keys import SubscriptionKey

def detect(imageURL):

    databasePath = "C:/Users/garvit/Desktop/Face Identification/face detect and track/Azure/people_database/"
    personGroupId = "0"

    # name: All the keys -> name mapping
    # identity: All the name -> keys mapping

    name = {}

    databases = os.walk(databasePath)
    databases = [database for database in databases][0][2]

    for databaseName in databases:
        file = open(databasePath + databaseName, 'r')
        dictionary = eval(file.read())

        print databaseName

        for key in dictionary:
            name[key] = dictionary[key]

    # print (str(len(name)) + " people retrieved")

    identity = {}
    for key in name:
        identity[name[key]] = key
    
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SubscriptionKey
    }

    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        # 'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses',
    })

    url = 'https://api.projectoxford.ai/face/v1.0/detect?%s' % params

    img = open(expanduser(imageURL), 'rb')
    response = requests.post(url, data=img, headers=headers)
    if response.status_code != 200:
        raise ValueError(
            'Request to Azure returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

    answer = response.json()
    faceId = answer[0]['faceId']

    # faceId generated, now face identify:

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SubscriptionKey
    }

    params = urllib.urlencode({
    })

    body = str({
        "personGroupId": personGroupId,
        "faceIds": [
            str(faceId)
        ],
        "maxNumOfCandidatesReturned": 5,
        "confidenceThreshold": 0
    })

    print(body)

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("Exception:" + str(e))

    answer = json.loads(data)

    print ("Response: " + str(answer))

    people = answer[0]['candidates']

    candidates = {}

    for person in people:
        candidates[name[person['personId']]] = person['confidence']

    with open('live-plot.txt', 'w') as outfile:
        json.dump(candidates, outfile)

    return name[people[0]['personId']], people[0]['confidence']
