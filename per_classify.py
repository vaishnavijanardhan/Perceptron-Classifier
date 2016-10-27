import json
import os
import sys

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

def predict(weights,b,filepath,fileFeatureDict):

    wordCounts = fileFeatureDict[filepath]
    #print("Word count", wordCounts)

    alpha = 0
    for word, wordCount in wordCounts.items():
        if(word in weights):
            wordWeight = weights[word]
        else:
            wordWeight = 0

        alpha += wordWeight*wordCount
    prediction = alpha + b

    return "spam" if prediction > 0 else "ham"


""" Start here **************** """

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

predictedLabels = []
#do prediction
for f in all_files:
    predictedLabel = predict(weights,b,f,fileFeatureDict)
    predictedLabels = predictedLabels + [predictedLabel]

#WRITE OUTPUT
writeFilePath = sys.argv[2]

writeContent = ""
for result in zip(all_files,predictedLabels):
    writeContent = writeContent + "{0} {1}".format(result[1],result[0]) + "\n"

outputfile = open(writeFilePath,"w", encoding="latin1")
outputfile.write(writeContent)
outputfile.close()