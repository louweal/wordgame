"""
Created on Sun Jun 11 12:45:50 2017

@author: louweal

This script parses all scraped data into a clean dataset
"""


import json
import pandas as pd
import numpy as np
import matplotlib as plt
#from pprint import pprint

sources = {
	"aspiecentral":"../aspiecentral/data/data_p1-p1152.jl",
	"atu2":"../atu2/data/atu2.jl",
	"gog":"../gog/data/data_p1-p5054.jl",
	"learn_english":"../learn-english/data/data_p1-p220.jl",
	"pinkbike":"../pinkbike/data/data_p1-p2747.jl",
	"sas":"../sas/data/sas.jl",
	"wrongplanet":"../wrongplanet/data/data_p1-p3825.jl"
}

def preprocess(x):
#	x = x.rstrip('!')
#	x = x.rstrip('.')
#	x = x.rstrip('?')
	x = x.split("(")[0]
	x = x.split(",")[0]
	x = x.split("*")[0]
	x = x.split("--")[0]	
	x = x.split("*")[0]
	x = x.split("\"")[0]	
	x = x.split(".")[0]		
	x = x.split("!")[0]		
	x = x.split("?")[0]
	x = x.split("=")[0]
	x = x.split("[")[0]		
	x = x.split(":")[0]		
	x = x.split(";")[0]		
	#x = x.split(" - ")[0]		
	x = x.rstrip(' ')
	x = x.lstrip(' ')
	return x

def parse(name, file):
	temp = {}

	data = []
	for line in open(file, 'r'):
		#print(line)
		data.append(json.loads(line))
	
	# convert data to pandas Dataframe
	datadf = pd.DataFrame(data)
	
	#remove first post in topic
	datadf = datadf.ix[1:] 	
	
	#authors to ids!	
	
	#converts list ['word'] to string 'word' 
	datadf['word'] = datadf['word'].apply(lambda x: ', '.join(x))

	#convert all to lowercase
	datadf['word'] = datadf['word'].apply(lambda x: x.lower())
	datadf['word'] = datadf['word'].apply(lambda x: preprocess(x))	

	#create pair with current word and previous word
	datadf['word1'] = datadf['word'].shift(1)	
	datadf['word2'] = datadf['word']
	datadf = datadf.drop('word', 1)



	
	# drop empty posts '' (row ids remain) [better method?]
	datadf = datadf.replace('',np.NaN)
	datadf = datadf.dropna(axis=0, how='any')
	
	
	datadf["source"] = name	
	
	temp['data'] = datadf	
	return temp


out_data = pd.DataFrame()
ppa = []
maxdup = []
meandup = []
freqwords = []
out = pd.DataFrame()

#parse sources in alphabetical order
for key, value in iter(sorted(sources.items())): 
	if(key == key):
		print("Parsing " +str(key) + "...")
		out = parse(key, value)
		#alldata = pd.concat([alldata, pd.DataFrame(out)])
		#combine datas		
		data = out['data']

		out_data = out_data.append(data, ignore_index=True)
		
		
		#posts
		#posts = len(out['data'])
		#print(posts)		
		
		#print first 10 rows
		#print(out['data'].head(10))

		ppa.append(round(data.groupby(['word2'])['author'].transform('count').mean(),2))
		maxdup.append((data['word2'].value_counts()).max())
		meandup.append((data['word2'].value_counts()).mean())
		freqwords.append(data['word2'].value_counts().head(15))


		

	
	
