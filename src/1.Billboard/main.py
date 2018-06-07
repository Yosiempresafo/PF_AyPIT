# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 01:43:11 2018

@author: LLara
"""
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter

class Billboard:
    @staticmethod
    def getLyricsList(path):
        csvarchivo = open(path)
        lista = []   
        for row in csvarchivo:
                lista.append(row.split(',')[4])
        del lista[0]
        return lista
    @staticmethod
    def get_ngrams(text, n):
        n_grams = ngrams(word_tokenize(text), n)
        return [' '.join(grams) for grams in n_grams]
    @staticmethod
    def getCounterNgram(pseudo, counter, n):
        ngrama=Billboard.get_ngrams(pseudo, n)
        counter.update(ngrama)
    @staticmethod
    def getCounter(lista, n):
        counter = Counter()
        for i in range(0, len(lista)):
            Billboard.getCounterNgram(lista[i], counter, n)
        return counter
    

lista = Billboard.getLyricsList('../../corpus/billboard_lyrics_1964-2015.csv')
c = Billboard.getCounter(lista, 3)
listaTop = c.most_common(100)


dicLove = {}
dicKnow={}
dicWant={}

for rola in lista:
    ng = Billboard.get_ngrams(rola,2)
    for n in ng:
        splitGram=n.split(' ')
        if splitGram[0]=="love" or splitGram[1]=="love":
            if splitGram[0]!="love":
                dicLove[splitGram[0]]= dicLove.get(splitGram[0], 0) + 1
            else:
                dicLove[splitGram[1]]= dicLove.get(splitGram[0], 0) + 1
        if splitGram[0]=="know" or splitGram[1]=="know":
            if splitGram[0]!="know":
                dicKnow[splitGram[0]]= dicKnow.get(splitGram[0], 0) + 1
            else:
                dicKnow[splitGram[1]]= dicKnow.get(splitGram[0], 0) + 1
        if splitGram[0]=="want" or splitGram[1]=="want":
            if splitGram[0]!="want":
                dicWant[splitGram[0]]= dicWant.get(splitGram[0], 0) + 1
            else:
                dicWant[splitGram[1]]= dicWant.get(splitGram[0], 0) + 1
            

from scipy.spatial import distance
love = (dicLove['i'],dicLove['you'],dicLove['in'], dicLove['your'], dicLove['that'], dicLove['dont'])
know = (dicKnow['i'],dicKnow['you'],dicKnow['in'], dicKnow['your'], dicKnow['that'], dicKnow['dont'])
want = (dicWant['i'],dicWant['you'],dicWant['in'], dicWant['your'], dicWant['that'], dicWant['dont'])

love2know = distance.euclidean(love,know)
know2Want = distance.euclidean(know,want)
want2Love = distance.euclidean(want,love)












