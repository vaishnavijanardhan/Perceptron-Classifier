import json
import os
import sys
from collections import Counter

def func_read_features(total_files):
    dict_features = {}
    word_features = {}
    for f in total_files:
        filestream = open(f,"r",encoding="latin1")
        file_content = filestream.read()
        tokens = file_content.split()
        word_features = dict(Counter(tokens))
        dict_features[f] = word_features
    return dict_features

def func_classify(total_f,dict_features,result):
    number_of_words = dict_features[total_f]
    for word, word_count in number_of_words.items():
        if(word in weights):
            w_word = weights[word]
        else:
             w_word = 0

        temp_var = w_word*word_count
        result = temp_var + result
    prediction = result + temp_fac

    return "spam" if prediction > 0 else "ham"

""" ***** Start here ***** """

write_file = sys.argv[2]
output_content = ""

with open('per_model.txt') as parameterfile:
    parameters = json.load(parameterfile)

global weights, temp_fac
weights = parameters[0]
temp_fac = parameters[1]


all_files = []
for drctry, drctry_name, file_name in os.walk(sys.argv[1]):
    for every_file in file_name:
        if ".txt" in every_file:
            all_files.append(os.path.join(drctry,every_file))

dict_features = func_read_features(all_files)

result = 0
do_classify = []
for f in all_files:
    belongs_to = func_classify(f,dict_features,result)
    do_classify = do_classify + [belongs_to]

out_file = open(write_file,"w", encoding="latin1")

for result in zip(all_files,do_classify):
    output_content = "{0} {1}".format(result[1],result[0]) + "\n" + output_content

out_file.write(output_content)
out_file.close()