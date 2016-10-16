import sys
import os
import json
from random import shuffle
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
    try:
        filestream = open(f,"r",encoding="latin1")
        content = filestream.read()
        tokens = content.split()
        wordFeatures = dict(Counter(tokens))
    except:
        print("Could not process file {0}".format(f))
    finally:
        filestream.close()
    return wordFeatures

def readAllWordFeatures(HamData, SpamData ):
    """
    read word frequency of all document
    """
    labelFilePathTuples = HamData + SpamData
    fileFeatureDict = {}

    for t in labelFilePathTuples:
        wordFeatures = readWordFeatures(t)
        fileFeatureDict[t[1]] = wordFeatures
    return fileFeatureDict

def trainPerceptron(labelFilePathTuples,fileFeatureDict,maxIteration=20):
    """
    For Ham, set Label = -1, for Spam, set Label = +1

    return (weights,b)
    """
    weights = {}
    b = 0
    for i in range(0,maxIteration):
        #randomize file index
        shuffle(labelFilePathTuples)

        for t in labelFilePathTuples:
            #f - filepath
            f = t[1]

            if t[0] == "ham":
                trueLabel = -1
            else:
                trueLabel = 1

            wordCounts = fileFeatureDict[f]

            alpha = 0
            for word, wordCount in wordCounts.items():
                if(word not in weights):
                    weights[word] = 0
                wordWeight = weights[word]

                alpha += wordWeight*wordCount
            #alpha is a prediction result
            alpha += b
            if(trueLabel * alpha <= 0):
                for word in wordCounts.keys():
                    weights[word] = weights[word] + trueLabel*wordCounts[word]
                b = b + trueLabel

    return (weights,b)

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

hamfiles_total=len(HamData)
spamfiles_total=len(SpamData)

HamData = [("ham",filepath) for filepath in HamData]
SpamData = [("spam",filepath) for filepath in SpamData]

fileFeatureDict = readAllWordFeatures(HamData, SpamData)

labelFilePathTuples = HamData + SpamData
parameters = trainPerceptron(labelFilePathTuples,fileFeatureDict)

with open('per_model.txt','w') as writefile:
    json.dump(parameters,writefile)

print("Done")