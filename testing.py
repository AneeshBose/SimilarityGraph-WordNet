#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:12:19 2019

@author: aneesh
"""

from nltk.corpus import wordnet as wn,stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import networkx as nx
import string
import math
import matplotlib.pyplot as plt

def remove_stopwrds(str):
    s = ""
    stopwrds = set(stopwords.words('english'))
    filtered = word_tokenize(str)
    for w in filtered:
        if w not in stopwrds and w not in string.punctuation:
            s += w
            s += " "
    return s

def SenseCount(wn_synset):
    data = list()
    for lemma in wn_synset.lemmas():
        c = 1 + lemma.count()
        data.append(c)
    return data


def cnt_wrd_freq(og,st):
    c = 0
    for d in og:
        if d == st:
            c += 1
    return c

def compute_min_max(mn,mx,rat):
    if rat == 1:
        return 1.2 * mx
    return mn + (mx-mn)*(-1/math.log(rat,2))
        

if __name__=="__main__":
    G = nx.DiGraph()
    sense_freq = list()
    ref = []
    G.add_node("chair")
    tot = 0
    syn = wn.synsets("chair")
    
    for x in syn:
        sense_freq = SenseCount(x)
        tot += sum(sense_freq)
        ref.append(sum(sense_freq)) 
        
    for x,y in zip(range(len(syn)),range(len(ref))):
        G.add_node(syn[x].definition())
        G.add_edge("chair",syn[x].definition(),weight=ref[y]*1.0/tot)
        
    #ADD DEFINITION EDGES
    def_wrds = []
    node = "the position of professor"
    def_wrds = word_tokenize(remove_stopwrds(node))
    co_ef = 1.0
    for wrd in def_wrds:
        if co_ef < 0.2:
            break;
        ratio = cnt_wrd_freq(def_wrds,wrd)*1.0/len(def_wrds)
        G.add_node(wrd)
        G.add_edge(node,wrd,weight=co_ef*compute_min_max(0.0,0.6,ratio))
        co_ef -= 0.2
        
    #ADD EXAMPLE USE EDGES
    ex_wrds = []
    node1 = str(wn.synsets("chair")[0].examples())
    nd = node1[3:]
    ex_wrds = word_tokenize(remove_stopwrds(nd))

    for wrd1 in ex_wrds:
        ratio = cnt_wrd_freq(ex_wrds,"chair")*1.0/len(ex_wrds)
        G.add_node(wrd1)
        G.add_edge(wn.synsets("chair")[0].definition(),wrd1,weight=compute_min_max(0.0,0.2,ratio))
        
        
    #ADD BACKWARD EDGES
    p = wn.synsets("chair")
    sense = 0
    for i in p:
        if "position" in i.definition():
            sense += 1
        
    for i in p:
        cnt = 0
        data = []
        data = word_tokenize(remove_stopwrds(i.definition()))
        for val in data:
            if val == "position":
               cnt += 1
        ratio = cnt*1.0/sense
        if ratio == 0:
            continue
        else:
            G.add_edge("position",i.definition(),weight=compute_min_max(0,0.3,ratio))
        
        
    nx.draw(G,with_labels=True,width=2)
    plt.savefig("a1.png")