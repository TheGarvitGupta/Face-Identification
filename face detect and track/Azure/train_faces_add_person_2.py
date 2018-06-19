# 2) Add people to the group

########### Python 2.7 #############
import httplib, urllib, base64, json
from keys import SubscriptionKey

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': SubscriptionKey,    
}

params = urllib.urlencode({
})

people = ["Garvit", "Emmanuel", "Wonkap", "Brian", "Nithin", "Obama"]
ids = []

for person in people:
	
	personGroupId = "100"
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

dict = {}

for i, j in zip(people, ids):
	dict[j] = i

print(dict)