import pandas as pd
import numpy as np
import json
import requests

req = requests.get('http://localhost:5000/receiveSkills')
datas = req.json()
skills = datas['data'][0]
skills1 = skills[0].split(",")
print(skills1)

data = pd.read_csv("UNIQUE_1.csv", index_col=0)
#print(data)
description = ['Python', 'java', 'C', 'Classification', 'nlp']
# skills = ['Python', 'java', 'C', 'Regression', 'convex optimisation', 'java', 'nlp', 'convex optimisation']


def unique(skills):
    s = set(skills)
    return list(s)

def convert_to_lowercase(array):
    array_lowercase = []
    for i in array:
        array_lowercase.append(i.lower())
    return array_lowercase

def dictionarise(desc, skil):
    d = {}
    for i in skil:
        for j in desc:
            if i == j:
                d[j] = True
            if j not in d and i != j:
                d[j] = False
    return d

def scorer1(desc, skil):
    score = 0
    desc_dictionary = dictionarise(desc, skil)
    for i in skil:
        if i in desc_dictionary.keys():
            if desc_dictionary[i] == True:
                score = score + 1


        else:

            semantic_score = 0
            for j in desc:
                semantic_score = semantic_score + data[i][j]

            semantic_score = semantic_score / len(desc)


            score = score + semantic_score
    score = score / len(desc)
    return min(1.0, score)

def interview_call(desc, skil, threshold):
    if scorer1(desc, skil) > threshold:
        req = requests.get('http://localhost:5000/sendMail')
        return print("main sent")

    else:
        return print("Thanks for applying")


if __name__== "__main__":

    skills = unique(skills1)
    print(skills)
    skills_lower = convert_to_lowercase(skills)
    description_lower = convert_to_lowercase(description)
    print(skills_lower, description_lower)
    print(scorer1(description_lower, skills_lower))
    interview_call(description_lower, skills_lower,0.7)

