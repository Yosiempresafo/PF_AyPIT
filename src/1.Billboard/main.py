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















