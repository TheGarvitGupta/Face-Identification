# 1) Create people group

import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '35f24aa856df408691c729b70e5f9e35',
}

params = urllib.urlencode({
})

personGroupId = "100"
body = str({
    "name": "100",
    "userData": "Database of faces of some people at BlueJeans, for a prototype of facial recognition in a video"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("PUT", "/face/v1.0/persongroups/" + personGroupId + "?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))