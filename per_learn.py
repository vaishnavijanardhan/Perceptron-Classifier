import sys
import os
import json

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