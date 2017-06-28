"""
Created on Sun Jun 11 12:45:50 2017

@author: louweal

Basic feature extraction script
"""


import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

#Word2Vec
from gensim.models.keyedvectors import KeyedVectors

df = pd.read_csv('../../data/processed/wordgame_201706.csv', dtype='object')
#store words as string
df['word1'] = df['word1'].astype('str') 
df['word2'] = df['word2'].astype('str') 

df['word1'] = df['word1'].map(str).apply(lambda x: x.lower())
df['word2'] = df['word2'].map(str).apply(lambda x: x.lower())

print('Loading word embeddings...')
w2v_model = KeyedVectors.load_word2vec_format('../../data/external/GoogleNews-vectors-negative300.bin', binary=True)

def similarity(r):

	if (r.word1 in w2v_model.vocab) & (r.word2 in w2v_model.vocab):
		wv1 = w2v_model.word_vec(r.word1)
		wv2 = w2v_model.word_vec(r.word2)
		
		return w2v_model.similarity(r.word1, r.word2)
	else:
		return 100


df['sim'] = df.apply(similarity, axis=1) 

ndf = df[df['sim'] <= 1.0]
lowlen = len(ndf)

'''





ppa = []
maxdup = []
meandup = []
freqwords = []
sample = []

		ppa.append(round(data.groupby(['word2'])['author'].transform('count').median(),2))
		maxdup.append((data['word2'].value_counts()).max())
		meandup.append((data['word2'].value_counts()).mean())
		freqwords.append(data['word2'].value_counts().head(30))
		sample.append(data['word2'].sample(15))


	#count final # of pairs
	pps.append(len(interm_data))

'''



