########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '35f24aa856df408691c729b70e5f9e35',
}

personGroupId = "100"
personName = "Garvit Gupta"
personId = "7c2577de-bd8e-47af-9df4-1ba8091e3114"

params = urllib.urlencode({
    # Request parameters
    'personGroupId': personGroupId,
    'personId': personId
})

body = str({
    # Request parameters
    "url": "https://qph.fs.quoracdn.net/main-thumb-81238783-200-ynjzkxcdcligttkzfnvrewwteaiwwehs.jpeg"
})

print (params)
print (body)

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId + "/persistedFaces?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

body = str({
    # Request parameters
    "url": "https://upload.wikimedia.org/wikipedia/commons/5/58/Garvit_Gupta_-_Headshot_400x400.jpg"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId + "/persistedFaces?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

body = str({
    # Request parameters
    "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUzXktCMryQfqmUATJaq4oBpLCGOFDIUPrwJQnD9xFjGEQu_fkMQ"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId + "/persistedFaces?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

body = str({
    # Request parameters
    "url": "https://i.stack.imgur.com/9E8eT.jpg?s=328&g=1"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId + "/persistedFaces?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

body = str({
    # Request parameters
    "url": "http://www.garvitgupta.com/images/Share/Facebook/FacebookOG.png"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId + "/persistedFaces?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))