# 2) Add people to the group

########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '35f24aa856df408691c729b70e5f9e35',
}

params = urllib.urlencode({
})

# Garvit Gupta
# {"personId":"7c2577de-bd8e-47af-9df4-1ba8091e3114"}

personGroupId = "100"
body = str({
    "name": "Garvit Gupta",
    "userData": "Software Engineer Intern"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Emmanuel Weber
# {"personId":"5ccf2619-7456-44c3-860d-ca1f894139dc"}

personGroupId = "100"
body = str({
    "name": "Emmanuel Weber",
    "userData": "VP, Engineering Meet-Me"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Brian Toombs
# {"personId":"f8e802da-c6d1-40f7-b0c0-286cd51aa8a0"}

personGroupId = "100"
body = str({
    "name": "Brian Toombs",
    "userData": "Senior Software Engineer"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Wonkap Jang
# {"personId":"cf66c514-ac7f-47ee-9e4b-b73eebecb5c8"}

personGroupId = "100"
body = str({
    "name": "Wonkap Jang",
    "userData": "Systems Architect, Video"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

# Nithin Prakash
# {"personId":"34c261c7-c2a8-44d9-8bd4-5d077e364f4e"}

personGroupId = "100"
body = str({
    "name": "Nithin Prakash",
    "userData": "Senior Software Engineer"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


# Adam Hyder
# {"personId":"f8005ddd-8046-420a-a7ed-bd8ccd3e3b50"}

personGroupId = "100"
body = str({
    "name": "Adam Hyder",
    "userData": "Sr. VP Engineering"
})

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))