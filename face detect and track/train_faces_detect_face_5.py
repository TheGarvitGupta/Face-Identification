import json, urllib, requests, httplib, base64

from pprint import pprint
from os.path import expanduser

def detect(imageURL):

	name = {'90b7d3f9-4fda-4df5-a847-a954d2677bab': 'Obama', '8bcd26d3-9931-480a-ad41-689566562d4e': 'Nithin', '7eacbf97-db79-4144-af03-2669b4028890': 'Brian', '4f4be214-ff3e-4917-946e-33ba51f6c285': 'Wonkap', '1a334200-950c-4c80-b98d-38caacf25f68': 'Emmanuel', '1eb50deb-7fd7-42c3-83a5-794af237af69': 'Garvit'}

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
	    "confidenceThreshold": 0
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