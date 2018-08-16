import gensim
from gensim.models import word2vec
import pandas as pd
import numpy as np
import jieba
import re
from functools import reduce


class Featurizer():
    def __init__(self,problems):
        self.data = [re.sub(ur"[:：?？,。，~_]+", "",s.decode('utf-8')) for s in problems]
        self.word_seg = [' '.join(jieba.cut(s,cut_all = False)).split(' ') for s in self.data]
    
    def word_embedding(self,Size,mincount):
        w2vmodel = word2vec.Word2Vec(self.word_seg,size = Size,min_count = mincount)
        feature_w2v = []
        for word in self.word_seg:
            temp = [w2vmodel[w] if w in w2vmodel else np.array(['1']) for w in word]
            temp2 = filter(lambda x: x[0] != '1', temp)
            if len(temp2) == 1: feature_w2v.append(temp2[0])
            elif len(temp2) == 0 : feature_w2v.append(np.zeros(Size))
            else: feature_w2v.append(reduce((lambda x, y: x + y), temp2)/float(len(temp2)))
        return np.array(feature_w2v)

class Label():
    def __init__(self,label):
        self.d,self.dnum = {},{}
        M = np.diag(np.ones(len(set(label))))
        for i,l in enumerate(list(set(label))):
            self.d[l] = M[i]
            self.dnum[l] = i
    def get_vector_label(self,label):
        L = []
        for l in label:
            L.append(self.d[l])
        return np.array(L)
    def get_num_label(self,label):
        L = []
        for l in label:
            L.append(self.dnum[l])
        return np.array(L)
        
        
#df = pd.read_csv('train.csv')
#df['Question']
#f = Featurizer(df['Question'])
#fea = f.word_embedding(100,5)
