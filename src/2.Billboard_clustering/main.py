# -*- coding: utf-8 -*-
"""
Created on Wed May  2 17:28:07 2018

@author: LLara
"""
import gensim
from gensim import corpora
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string

def getLyricsList(path):
        csvarchivo = open(path)
        lista = []   
        for row in csvarchivo:
                lista.append(row.split(',')[4])
        del lista[0]
        return lista

        
lista = getLyricsList('../../corpus/billboard_lyrics_1964-2015.csv')
       
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


doc_clean= [clean(doc).split() for doc in lista]  

dictionary = corpora.Dictionary(doc_clean)

doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

Lda = gensim.models.ldamodel.LdaModel

ldamodel = Lda(doc_term_matrix, num_topics=50, id2word = dictionary, passes=50)

print(ldamodel.print_topics(num_topics=30, num_words=10))
