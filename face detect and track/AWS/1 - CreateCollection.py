import boto3

if __name__ == "__main__":

	client=boto3.client('rekognition')
	response = client.create_collection(CollectionId='myphotos')
	print(response)