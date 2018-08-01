# Reads the dictionaries in the given directory and converts to main.json in the same directory

import os, json

def files(JSONdirectory):
    # Returns list of absolute paths for directory files
    directory = os.walk(JSONdirectory)
    files = [file for file in directory][0][2]

    fileURIs = []
    for file in files:
        fileURIs.append(JSONdirectory + '/' + file)

    return fileURIs

# json.dump(data, fp, sort_keys=True, indent=4)

directory = "C:/Users/garvit/Desktop/AWS/Map"

jsonFiles = files(directory)
dictionary = {}
tempDictionary = {}

for file in jsonFiles:
	with open(file, 'r') as F:
		tempDictionary = eval(F.read())

	for key in tempDictionary:
		dictionary[key] = tempDictionary[key]

with open(directory + '/main.json', 'w') as F_JSON:
    json.dump(dictionary, F_JSON, sort_keys=True, indent=4)