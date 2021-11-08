from collections import Counter, OrderedDict
from itertools import product
import matplotlib.pyplot as plt
from random import *


import numpy as np
import string
import sys
import re
import math

'''
Code was used as an assignment for CS540: Intro to AI at the University of Wisconsin. Starter code was provided by
the TA for the course and is called out in the comments below.
'''

with open('Avengers_Script.txt') as f: #replace with any script or document in .txt format here
    data = f.read()

#TA starter code
data = data.lower()
data = data.translate(str.maketrans('', '', string.punctuation))
data = re.sub('[^a-z]+', ' ', data)
data = ' '.join(data.split(' ')) #convert the entire document into parsable data

allchar = ' ' + string.ascii_lowercase #initialize a variable with all lowercase ascii charachters and the whitespace charachter
#End TA starter code

unigram = Counter(data) #unigram is just the count of each charachter, use a Counter object for that
unigram_prob = {ch: round((unigram[ch]) / (len(data)), 4) for ch in allchar} #unigram probability is just the frequency of charachter over the total data
uni_list = [unigram_prob[c] for c in allchar] #place all unigram probs in a list
'''
#write unigram probs into a txt file
with open('unigram_prob.txt', 'a') as file:
    for key in unigram_prob:
        file.write(str(unigram_prob[key])+",")
'''

#TA starter code
def ngram(n):
    # all possible n-grams
    d = dict.fromkeys([''.join(i) for i in product(allchar, repeat=n)],0)
    # update counts
    d.update(Counter([''.join(j) for j in zip(*[data[i:] for i in range(n)])]))
    return d
#End TA starter code

bigram = ngram(2)  # c(ab)
bigram_prob = {c: bigram[c] / unigram[c[0]] for c in bigram}  # p(b|a)
bigram_prob_list = []
i = 0
s = 0
l = []
for key in bigram_prob: #create a list of bigram probabilities for each charachter based on the prob of the previous charachter
    i += 1
    if i % 27 == 0:
        l.append(1 - s)
        bigram_prob_list.append(l)
        l = []
        s = 0
    else:
        l.append(bigram_prob[key])
        s += bigram_prob[key]


#Laplace smoothing to prevent a zero probability combination occuring
bigram_prob_laplace = {c: (bigram[c] + 1) / (unigram[c[0]] + 27) for c in bigram}

i = 0
s = 0
l = []
bigram_prob_laplace_list = []
for key in bigram_prob_laplace:
    i += 1
    if i % 27 == 0:
        if bigram_prob_laplace[key] < 0.0001:
            l.append(0.0001)
            bigram_prob_laplace_list.append(l)
            l = []
        else:
            l.append(round(bigram_prob_laplace[key],4))
            bigram_prob_laplace_list.append(l)
            l = []
    else:
        if bigram_prob_laplace[key] < 0.0001:
            l.append(0.0001)
        else:
            l.append(round(bigram_prob_laplace[key],4))


'''
#Print output for bigram probability into text file
with open('bigram_prob.txt', 'a') as file:
    for i in bigram_prob_list:
        for j in i:
            file.write(str(j) + ",")
        file.write("\n")
'''

'''
#Print output for bigram probability with laplace smoothing into text file
with open('bigram_prob_laplace.txt', 'a') as file:
    for i in bigram_prob_laplace_list:
        for j in i:
            file.write(str(j) + ",")
        file.write("\n")
'''

trigram = ngram(3)
trigram_prob = {c: (trigram[c] + 1) / (bigram[c[:2]] + 27) for c in trigram}


#TA starter code
def gen_bi(c):
    w = [bigram_prob[c + i] for i in allchar]
    return choices(allchar, weights=w)[0]


def gen_tri(ab):
    w_tri = [trigram_prob[ab + i] for i in allchar]
    return choices(allchar, weights=w_tri)[0]
#End TA starter code

#function to generate a sentance based on a charachter (c) and a length of sentance (num)
def gen_sen(c, num):
    res = c + gen_bi(c)
    for i in range(num - 2):
        if bigram[res[-2:]] == 0:
            t = gen_bi(res[-1])
        else:
            t = gen_tri(res[-2:])
        res += t
    return res

example_sentence = gen_sen('h', 100)


#Write out the file with 1000 charachter sentances beginning with each letter
with open('newscript.txt', 'a') as file:
    for c in allchar[1:]:
        sentance = gen_sen(c,1000)
        file.write(sentance + "\n")
