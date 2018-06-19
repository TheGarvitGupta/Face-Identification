import json, urllib, requests, httplib, base64

from pprint import pprint
from os.path import expanduser

def detect(imageURL = "C:/Users/garvit/Desktop/garvit.jpeg"):

	name = {
		"7c2577de-bd8e-47af-9df4-1ba8091e3114": "Garvit Gupta",
		"5ccf2619-7456-44c3-860d-ca1f894139dc": "Emmanuel Weber",
		"f8e802da-c6d1-40f7-b0c0-286cd51aa8a0": "Brian Toombs",
		"cf66c514-ac7f-47ee-9e4b-b73eebecb5c8": "Wonkap Jang",
		"34c261c7-c2a8-44d9-8bd4-5d077e364f4e": "Nithin Prakash",
		"f8005ddd-8046-420a-a7ed-bd8ccd3e3b50": "Adam Hyder",
	}

	headers = {
	    'Content-Type': 'application/octet-stream',
	    'Ocp-Apim-Subscription-Key': '35f24aa856df408691c729b70e5f9e35',
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
	    'Ocp-Apim-Subscription-Key': '35f24aa856df408691c729b70e5f9e35',
	}

	params = urllib.urlencode({
	})

	body = str({
	    "personGroupId": "100",
	    "faceIds": [
	        str(faceId)
	    ],
	    "maxNumOfCandidatesReturned": 1,
	    "confidenceThreshold": 0.1
	})

	try:
	    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
	    response = conn.getresponse()
	    data = response.read()
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	answer = json.loads(data)
	personId = answer[0]['candidates'][0]['personId']
	confidence = answer[0]['candidates'][0]['confidence']

	print("Identified:", name[personId], confidence)	

	return name[personId], confidence