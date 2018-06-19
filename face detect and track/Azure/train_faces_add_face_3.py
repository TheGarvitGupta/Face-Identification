########### Python 2.7 #############
import httplib, urllib, base64
from keys import SubscriptionKey

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': SubscriptionKey,
}

name = {'90b7d3f9-4fda-4df5-a847-a954d2677bab': 'Obama', '8bcd26d3-9931-480a-ad41-689566562d4e': 'Nithin', '7eacbf97-db79-4144-af03-2669b4028890': 'Brian', '4f4be214-ff3e-4917-946e-33ba51f6c285': 'Wonkap', '1a334200-950c-4c80-b98d-38caacf25f68': 'Emmanuel', '1eb50deb-7fd7-42c3-83a5-794af237af69': 'Garvit'}
identity = {}

for key in name:
    identity[name[key]] = key

personGroupId = "100"

personId = identity['']
urls = [
''
]

for url in urls:
    params = urllib.urlencode({
        # Request parameters
        'personGroupId': personGroupId,
        'personId': personId
    })

    body = str({
        # Request parameters
        "url": url
    })

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