import boto3, os, time

def images(personName, officePath):
    # Returns list of absolute image paths for person name and office path (absolute)
    directory = officePath + "/" + personName
    images = os.walk(directory)
    images = [image for image in images][0][2]
    imageURLs = []
    for image in images:
        imageURLs.append(directory + '/' + image)
    return imageURLs

folderPath = "C:/Users/garvit/Desktop/Extract Images/Mountain View - 520"
people = os.walk(folderPath)
people = sorted([person for person in people][0][1])

client=boto3.client('rekognition')

FaceIdPerson = {}

for person in people:
	print(person)
	for imageFile in images(person, folderPath):
		print("\t" + imageFile)
		with open(imageFile, 'rb') as image:
			response = client.index_faces(CollectionId='myphotos', DetectionAttributes=[], Image={'Bytes': image.read()})
			print(response)
		try:
			faceId = response["FaceRecords"][0]["Face"]["FaceId"]
			FaceIdPerson[faceId] = person
		except(IndexError):
			print("No face found")
		time.sleep(0.1)
	print

print(FaceIdPerson)

file = open("Map/" + '%d.txt' % time.time(), 'w+')
file.write(str(FaceIdPerson))