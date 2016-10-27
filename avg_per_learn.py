import sys
import os
import random
import json
from collections import Counter

def readAllWordFeatures(SpamData, HamData):
    labelFilePathTuples = SpamData + HamData

    fileFeatureDict = {}
    wordFeatures = {}

    for t in labelFilePathTuples:
        f = t[1]
        filestream = open(f,"r",encoding="latin1")
        content = filestream.read()
        tokens = content.split()
        wordFeatures = dict(Counter(tokens))
        filestream.close()
        #wordFeatures = readWordFeatures(each_f) #readWordFeatures function
        fileFeatureDict[t[1]] = wordFeatures
    return fileFeatureDict

def trainPerceptron(HamData,SpamData,fileFeatureDict):
    """
    For Ham, set Label = -1, for Spam, set Label = -1
    return (weights,b)
    """
    labelFilePathTuples = HamData + SpamData
    random.shuffle(labelFilePathTuples)
    weights = {}
    b = 0
    for i in range(0,20):
        #randomize file index
        #random.shuffle(labelFilePathTuples)
        for t in labelFilePathTuples:
            if t[0] == "spam":
                trueLabel = 1
            else:
                trueLabel = -1

            wordCounts = fileFeatureDict[t[1]]

            alpha = 0
            for word, wordCount in wordCounts.items():
                if(word not in weights):
                    weights[word] = 0

                wordWeight = weights[word]
                alpha = alpha + wordCount*wordWeight

            alpha = alpha + b
            if((trueLabel * alpha > 0)!=1):
                for word in wordCounts.keys():
                    weights[word] = weights[word] + trueLabel*wordCounts[word]
                b = b + trueLabel

    return (weights,b)


def getHam():
    return [("ham",filepath) for filepath in HamData]

def getSpam():
    return [("spam",filepath) for filepath in SpamData]

""" *********** START HERE *************** """
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


# Training the learner with only 10% of the data

folder_train = 0.1
random.seed(100)

total_files = len(HamData) + len(SpamData)
total_train_files = int(round(folder_train*total_files*0.5))
HamData = random.sample(HamData,total_train_files)
SpamData = random.sample(SpamData,total_train_files)

HamData = getHam()
SpamData = getSpam()

print(len(HamData))
print(len(SpamData))

fileFeatureDict = readAllWordFeatures(HamData, SpamData)
parameters_model = trainPerceptron(HamData, SpamData, fileFeatureDict)

with open('per_model.txt','w') as writefile:
     json.dump(parameters_model,writefile)