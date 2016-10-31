import sys
import os
import random
import json
from collections import Counter

def func_read_features(SpamData, HamData):

    total_training_files = SpamData + HamData
    dict_features = {}
    word_features = {}

    for each_file in total_training_files:
        f = each_file[1]
        filestream = open(f,"r",encoding="latin1")
        file_content = filestream.read()
        tokens = file_content.split()
        word_features = dict(Counter(tokens))
        filestream.close()
        dict_features[each_file[1]] = word_features
    return dict_features

def func_perceptron(HamData,SpamData,dict_features):

    total_training_files = HamData + SpamData
    random.shuffle(total_training_files)
    weights = {}
    for i in range(0,20):
        for each_file in total_training_files:
            if each_file[0] == "spam":
                file_label = 1
            else:
                file_label = -1

            number_of_words = dict_features[each_file[1]]

            result = 0
            for word, word_count in number_of_words.items():
                if(word not in weights):
                    weights[word] = 0
                else:
                    w_word = weights[word]
                    temp_var = word_count*w_word
                    result =  result + temp_var


            temp_factor = 0
            result = result + temp_factor

            if((file_label * result > 0) != 1):
                for word in number_of_words.keys():
                    weights[word] = file_label*number_of_words[word] + weights[word]
                temp_factor = file_label + temp_factor

    return (weights,temp_factor)


def getHam():
    return [("ham",filepath) for filepath in HamData]

def getSpam():
    return [("spam",filepath) for filepath in SpamData]

""" ***** START HERE ***** """
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

""" Training the learner with only 10% of the data
total_files = len(HamData) + len(SpamData)
total_train_files = int(round(0.1*total_files*0.5))
HamData = random.sample(HamData,total_train_files)
SpamData = random.sample(SpamData,total_train_files) """

HamData = getHam()
SpamData = getSpam()

dict_features = func_read_features(HamData, SpamData)
model_file = func_perceptron(HamData, SpamData, dict_features)

with open('per_model.txt','w') as output_file:
     json.dump(model_file,output_file)