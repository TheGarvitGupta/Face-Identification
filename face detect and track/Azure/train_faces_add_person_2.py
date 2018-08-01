# 2) Add people to the group

########### Python 2.7 #############
import httplib, urllib, base64, json
from keys import SubscriptionKey
import os
import time

# The absolute path to the folder that contains a folder for each person
folderPath = "C:/Users/garvit/Desktop/Extract Images/Mountain View - 520"
people = os.walk(folderPath)
people = sorted([person for person in people][0][1])

personGroupId = "0"
databasePath = "people_database/"

if not os.path.exists(databasePath):
    os.makedirs(databasePath)

print("Found " + str(len(people)) + " people: " + str(people))

file = open(databasePath + '%d.txt' % time.time(), 'w+')

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': SubscriptionKey,    
}

params = urllib.urlencode({
})

ids = []

for person in people:

	print ("Processing", person)
	
	body = str({
	    "name": person
	})

	try:
	    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, body, headers)
	    response = conn.getresponse()
	    data = response.read()
	    print(data)
	    ids.append(json.loads(data)['personId'])
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

peopleDict = {}

for i, j in zip(people, ids):
	peopleDict[j] = i

file.write(str(peopleDict))
file.close()

print("Completed:")
print(peopleDict)