"""
Created on Sun Jun 11 12:45:50 2017

@author: louweal

Basic feature extraction script
"""


import Levenshtein
import pandas as pd
import numpy as np

def levenshtein(r):
#	return 1
	return Levenshtein.distance(r.word1, r.word2)


#read input data
infile = pd.read_csv('../../data/processed/wordgame_201706.csv')

#create new dataframe
df = pd.DataFrame(infile)
df['sourceID'] = df['source'].astype('category').cat.codes	

df['word1'] = df['word1'].map(str)
df['word2'] = df['word2'].map(str)


df['len1'] = df['word1'].apply(lambda x:len(x))
df['len2'] = df['word2'].apply(lambda x:len(x))

print("Min word length: "+ str(df['len2'].min()))
print("Max word length: "+ str(df['len2'].max()))
print("Mean word length: "+ str(df['len2'].mean()))

df['edit'] = df.apply(levenshtein, axis=1)

print("Mean edit distance: "+ str(df['edit'].mean()))

#subset common word lengths
sdf = df[(2 < df['len1']) & (df['len1'] < 18) & (2 < df['len2']) & (df['len2'] < 18)]


med = np.zeros(shape=(10,1)) # mean edit distance difference 

df10 = pd.DataFrame()
df10 = df10.append(pd.DataFrame([0,1, 2,3,4,5,6,7,8,9]))
#df10['len'] = df.apply()

for i in range(0,10):
	small = sdf[(sdf['sourceID'] == i)]
	med[i,0] = small['edit'].mean()
		


np.set_printoptions(precision=4)
print(med)		

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



