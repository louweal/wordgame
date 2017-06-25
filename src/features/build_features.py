"""
Created on Sun Jun 11 12:45:50 2017

@author: louweal

Basic feature extraction script
"""


import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sb

import Levenshtein


def levenshtein(r):
#	return 1
	return Levenshtein.distance(r.word1, r.word2)

#
def isNt(r):
	return ((r.sourceID%9)>0)

#read input data
infile = pd.read_csv('../../data/processed/wordgame_201706.csv')

#create new dataframe
df = pd.DataFrame(infile)
df['sourceID'] = df['source'].astype('category').cat.codes	
df['nt'] = df.apply(isNt, axis=1)

df['word1'] = df['word1'].map(str)
df['word2'] = df['word2'].map(str)


df['len1'] = df['word1'].apply(lambda x:len(x))
df['len2'] = df['word2'].apply(lambda x:len(x))

print("Min word length: "+ str(df['len2'].min()))
print("Max word length: "+ str(df['len2'].max()))
print("Mean word length: "+ str(df['len2'].mean()))

#Plot word lengths

#Remove outliers 
#df = ...


df['edit'] = df.apply(levenshtein, axis=1)
#save interm!

print("Mean edit distance: "+ str(df['edit'].mean()))

#delete outliers in terms of word length
df = df[(2 < df['len1']) & (df['len1'] < 18) & (2 < df['len2']) & (df['len2'] < 18)]

nt = df[(df['sourceID'] != 9) & (df['sourceID'] != 0)]
asd = df[(df['sourceID'] == 9) | (df['sourceID'] == 0)]

#normalize?
#nt['edit'] = nt['edit']/nt['edit'].max().astype(np.float64)
#asd['edit'] = asd['edit']/asd['edit'].max().astype(np.float64)


weights_nt = np.ones_like(nt['edit'])/len(nt['edit'])
weights_asd = np.ones_like(asd['edit'])/len(asd['edit'])

nt['edit'].plot.hist(by='edit', bins=15, alpha=0.5, label='NT', weights=weights_nt)
asd['edit'].plot.hist(by='edit', bins=15, alpha=0.5, label='ASD', weights=weights_asd)
#plt.legend(loc='upper right')








edit = np.zeros(shape=(10,1)) # mean edit distance difference 

df10 = pd.DataFrame()
df10 = df10.append(pd.DataFrame([0,1, 2,3,4,5,6,7,8,9]))
#df10['len'] = df.apply()

for i in range(0,10):
	small = df[(df['sourceID'] == i)]
	edit[i,0] = small['edit'].mean()
		


np.set_printoptions(precision=4)
print(edit)		

''''
#Word2Vec
from gensim.models.keyedvectors import KeyedVectors


print('Loading word embeddings...')
w2v_model = KeyedVectors.load_word2vec_format('../../data/external/GoogleNews-vectors-negative300.bin', binary=True)

def similarity(r):
    found       = False
    normalized  = False
    word_vector = None

    # If word in vocab as-is vectorize
    if r.word1 in w2v_model.vocab:
        found       = True
        word_vector = w2v_model.word_vec(word)
	
	word_vectors.similarity(r.word1, r.word2)
	return word_vector

for r in df:
	
df['sim'] = df.apply(similarity, axis=1) 









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



