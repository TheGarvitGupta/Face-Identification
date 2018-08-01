import boto3

def getName(faceId, mapPath):
	file = open(mapPath, "r")
	FaceIdPerson = eval(file.read())
	return FaceIdPerson[faceId]

def detectAWS(imageURL):
	client=boto3.client('rekognition')
	with open(imageURL, 'rb') as image:
		response=client.search_faces_by_image(CollectionId='myphotos', Image={'Bytes': image.read()}, FaceMatchThreshold=0, MaxFaces=1)
		print(response)
	faceMatches=response['FaceMatches']
	for match in faceMatches:
		return match['Face']['FaceId'], "{:.2f}".format(match['Similarity'])

def rekognize(imageURL='C:/Users/garvit/Desktop/Extract Images/garvit.jpg'):
	mapPath = 'C:/Users/garvit/Desktop/AWS/Map/main.json'
	faceId, confidence = detectAWS(imageURL)
	name = getName(faceId, mapPath)
	return name, confidence

print(rekognize())