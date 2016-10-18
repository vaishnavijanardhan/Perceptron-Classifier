import json
import os
import sys

""" Start here """


def readAllWordFeatures(filelpaths):
    fileFeatureDict = {}

    for f in filelpaths:
        wordFeatures = readWordFeatures(f)
        fileFeatureDict[f] = wordFeatures
    return fileFeatureDict

def readWordFeatures(filepath):
    wordFeatures = {}

    try:
        filestream = open(filepath,"r",encoding="latin1")
        content = filestream.read()
        tokens = content.split()
        for token in tokens:
            if(token in wordFeatures):
                wordFeatures[token] = wordFeatures[token] + 1
            else:
                wordFeatures[token] = 1
    except:
        print("Could not process file {0}".format(f))
    finally:
        filestream.close()
    return wordFeatures

with open('per_model.txt') as parameterfile:
    parameters = json.load(parameterfile)

weights = parameters[0]
b = parameters[1]

#files to be predicted
all_files = []
for drctry, drctry_name, file_name in os.walk(sys.argv[1]):
    for every_file in file_name:
        if ".txt" in every_file:
            all_files.append(os.path.join(drctry,every_file))

fileFeatureDict =readAllWordFeatures(all_files)
#print(fileFeatureDict)