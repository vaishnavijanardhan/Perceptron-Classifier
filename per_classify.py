import json
import os
import sys
from collections import Counter

def readAllWordFeatures(filelpaths):
    fileFeatureDict = {}
    wordFeatures = {}
    for f in filelpaths:
        filestream = open(f,"r",encoding="latin1")
        content = filestream.read()
        tokens = content.split()
        wordFeatures = dict(Counter(tokens))
        fileFeatureDict[f] = wordFeatures
    return fileFeatureDict

def predict(filepath,fileFeatureDict,alpha):
    wordCounts = fileFeatureDict[filepath]
    for word, wordCount in wordCounts.items():
        if(word in weights):
            wordWeight = weights[word]
        else:
             wordWeight = 0

        temp_var = wordWeight*wordCount
        alpha = temp_var + alpha
    prediction = alpha + b

    return "spam" if prediction > 0 else "ham"

""" Start here **************** """

writeFilePath = sys.argv[2]
writeContent = ""

with open('per_model.txt') as parameterfile:
    parameters = json.load(parameterfile)

global weights, b
weights = parameters[0]
b = parameters[1]

#files to be predicted
all_files = []
for drctry, drctry_name, file_name in os.walk(sys.argv[1]):
    for every_file in file_name:
        if ".txt" in every_file:
            all_files.append(os.path.join(drctry,every_file))

fileFeatureDict = readAllWordFeatures(all_files)

alpha = 0
predictedLabels = []
for f in all_files:
    predictedLabel = predict(f,fileFeatureDict,alpha)
    predictedLabels = predictedLabels + [predictedLabel]

outputfile = open(writeFilePath,"w", encoding="latin1")

for result in zip(all_files,predictedLabels):
    writeContent = "{0} {1}".format(result[1],result[0]) + "\n" + writeContent

outputfile.write(writeContent)
outputfile.close()