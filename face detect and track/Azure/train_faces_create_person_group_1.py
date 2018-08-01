# 1) Create people group

import httplib, urllib, base64
from keys import SubscriptionKey

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': SubscriptionKey,
}

params = urllib.urlencode({
})

personGroupId = "0"
body = str({
    "name": "0",
    "userData": "Experimental Database"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    # Replace PUT with DELETE to delete the group and the members
    conn.request("PUT", "/face/v1.0/persongroups/" + personGroupId + "?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))