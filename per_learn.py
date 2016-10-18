import sys
import os
import json
import random
from collections import Counter

def learnModel(diction,data):
    for each_file in data:
            filest = open(each_file,"r",encoding="latin1")
            file_content = filest.read()
            tokens = file_content.split()
            for each_token in tokens:
                if(each_token in diction):
                    diction[each_token] = diction[each_token] + 1
                else:
                    diction[each_token] = 1
            filest.close()


def readWordFeatures(labelFilePathTuple):

    wordFeatures = {}
    f = labelFilePathTuple[1]
    filestream = open(f,"r",encoding="latin1")
    content = filestream.read()
    tokens = content.split()
    wordFeatures = dict(Counter(tokens))

    filestream.close()
    return wordFeatures


def readAllWordFeatures(SpamData, HamData):
    """ read word frequency of all document """
    global labelFilePathTuples
    labelFilePathTuples = SpamData + HamData
#print(labelFilePathTuples)
    fileFeatureDict = {}

    for each_f in labelFilePathTuples:
        wordFeatures = readWordFeatures(each_f) #readWordFeatures function
        fileFeatureDict[each_f[1]] = wordFeatures
    return fileFeatureDict


def trainPerceptron(fileFeatureDict):
    """ For Ham, set Label = +1, for Spam, set Label = -1
    return (weights,beta) """
    weights = {}
    for i in range(0,20):
        #randomize file index
        random.shuffle(labelFilePathTuples)

        for t in labelFilePathTuples:
            #f - filepath
            f = t[1]

            if t[0] == "ham":
                trueLabel = +1
            else:
                trueLabel = -1

            wordCounts = fileFeatureDict[f]

            alpha = 0
            for word, wordCount in wordCounts.items():
                if(word not in weights):
                    weights[word] = 0
                wordWeight = weights[word]

                count = wordWeight * wordCount
                alpha = alpha + count
            #alpha is a prediction result
            beta = 0
            alpha = alpha + beta
            if(trueLabel * alpha <= 0):
                for word in wordCounts.keys():
                    weights[word] = weights[word] + trueLabel*wordCounts[word]
                beta = beta + trueLabel

    return (weights,beta)

""" **************** START HERE ******************** """

#list of all files
HamData = []
SpamData = []

if len(sys.argv) < 2:
    print("Error: The input data path is NULL or empty\n")
    sys.exit(-1)

for drctry, drctry_name, file_name in os.walk(sys.argv[1]):
    for every_file in file_name:
        if ".txt" in every_file:
            if "ham" in every_file:
                HamData.append(os.path.join(drctry,every_file))
            else:
                 SpamData.append(os.path.join(drctry,every_file))

random.shuffle(HamData)
random.shuffle(SpamData)

HamData = [("ham",filepath) for filepath in HamData]
SpamData = [("spam",filepath) for filepath in SpamData]

#read features of all files (cached)
fileFeatureDict = readAllWordFeatures(SpamData, HamData) #readAllWordFeatures FUNCTION

parameters = trainPerceptron(fileFeatureDict)

with open('per_model.txt','w') as writefile:
     json.dump(parameters,writefile)


