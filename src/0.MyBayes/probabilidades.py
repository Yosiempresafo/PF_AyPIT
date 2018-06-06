# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 16:41:05 2018

@author: LLara
"""
from collections import Counter

class Bayes:
    @staticmethod
    def generarCategos(*listas):
        dic={}
        count=0
        for lista in listas:
            dic[count]=lista
            count=count+1            
        return dic
    @staticmethod
    def generarDicTypes(*listas):
        count=0
        dic={}
        for lista in listas:
            for x in lista:
                if not x in dic.values():
                    dic[count]=x
                    count=count+1            
        return dic
    @staticmethod
    def probCatego(categorias, index):
        countCatego=0
        for categoria in categorias.values():
            countCatego=countCatego + len(categoria)
        return len(categorias[index])/countCatego
    @staticmethod  
    def probTypeCatego(tipo, catego):
        c=Counter(catego)
        return c[tipo]/len(catego)
    @staticmethod
    def probType(tipo, categos):
        prob=0
        for x in range(0,len(categos)):
            pc=Bayes.probCatego(categos, x)
            ptc=Bayes.probTypeCatego(tipo, categos[x])
            prob=prob + (pc*ptc)
        return prob
    @staticmethod
    def probTypes(categos, m):
        prob=0
        ptc=1
        res=[((key*0)+1) for key in categos]
        for mensaje in m:
            for x in range(0,len(categos)):
                res[x]=res[x]*Bayes.probTypeCatego(mensaje, categos[x])
        for x in range(0,len(categos)):
            pc=Bayes.probCatego(categos, x)
            ptc=res[x]
            prob=prob + (pc*ptc)
        return prob
    @staticmethod
    def bayes(categos, index, tipo):
        pba=Bayes.probTypeCatego(tipo, categos[index])
        pa=Bayes.probCatego(categos,index)
        pb=Bayes.probType(tipo,categos)
        return (pba*pa)/pb
    @staticmethod
    def bayesLista(categos, index, m):
        pba=1
        for mensaje in m:
            pba=pba*Bayes.probTypeCatego(mensaje, categos[index])
        pa=Bayes.probCatego(categos,index)
        pb=Bayes.probTypes(categos, m)
        return (pba*pa)/pb

class BayesLaplace:
    @staticmethod
    def laplaceSmoothing(categos, index, m, k):
        
        return
    @staticmethod
    def probCatego(categos, index,k):
        countCatego=0
        for categoria in categos.values():
            countCatego=countCatego + len(categoria)
        res=len(categos[index])/countCatego
        a=(countCatego*res)+k
        b=(len(categos[index])/res)+len(categos)
        #print(a/b)
        #print(len(categos[index])/(countCatego))
        return (len(categos[index])+k)/(countCatego+len(categos))
    @staticmethod  
    def probTypeCatego(tipo, catego):
        c=Counter(catego)
        return c[tipo]/len(catego)
    
            
spam=["oferta","es","secreto","click","secreto","link","secreto","deportes","link"]
ham=["juega","deportes","hoy","fue","juega","deportes","secreto","deportes","eventos","deportes","es","hoy","deportes","cuesta","dinero"]

dicTypes=Bayes.generarDicTypes(spam,ham)
categos=Bayes.generarCategos(spam,ham)
spamProb=Bayes.probCatego(categos, 0)

dosInSpam=Bayes.probTypeCatego(dicTypes[2],categos[0])
dosInHam=Bayes.probTypeCatego(dicTypes[2],categos[1])

#lKey = [key for key, value in dicTypes.items() if value == "es"][0]

probSpamSeis=Bayes.bayes(categos, 0, dicTypes[5])
pb=Bayes.bayesLista(categos, 0, [dicTypes[2], dicTypes[1], dicTypes[2]])


