# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 18:48:58 2018

@author: LLara
"""

import numpy as np
#import time
import pandas as pd
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB


print("Is love (?) <3")
print()

filee = open('../../corpus/corpusBillboardCaracterizado.csv')

X=[]  
y=[]
for line in filee:
    lineArray=line.split(' ')
    tweet=lineArray[0]
    sentiement=lineArray[1]
    listaTmp= list(map(int, tweet))
    X.append(listaTmp)
    y.append(sentiement)
    
X = np.asarray(X)
y = np.asarray(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)

gnb = GaussianNB()
gnb.fit(X_train, y_train)
 
y_pred = gnb.predict(X_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix")
print(cm)
a = cm.shape
corrPred = 0
falsePred = 0

for row in range(a[0]):
    for c in range(a[1]):
        if row == c:
            corrPred +=cm[row,c]
        else:
            falsePred += cm[row,c]
print('Correct predictions ->', corrPred)
print('False predictions ->', falsePred)

print()
print("Results")
precision= round((corrPred/(cm.sum()))*100 * 1000 / 1000,2)
recall = round(metrics.recall_score(y_test, y_pred, average='macro')*100*1000/1000,2)
f1=round(2*((precision*recall)/(precision+recall))*1000/1000,2)

print("Accuracy: ", precision,"%")
print("Recall: ", recall,"%")
print("F1: ", f1, "%")
#print(gnb.score(X_test, y_test)) #otro método
