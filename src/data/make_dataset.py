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

sources = { #sources in alphabetical order 
	"aspiecentral":"../../data/raw/aspiecentral.jl",
	"atu2":"../../data/raw/atu2.jl",
	"bleeping_computer":"../../data/raw/bleeping_computer5.jl",
	"ecig":"../../data/raw/ecig.jl",
	"gog":"../../data/raw/gog.jl",
	"learn_english":"../../data/raw/learn-english.jl",
	"pinkbike":"../../data/raw/pinkbike.jl",
	"sas":"../../data/raw/sas.jl",
	"the_fishy":"../../data/raw/the_fishy.jl",
	"wrongplanet":"../../data/raw/wrongplanet.jl"
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

dropped = []
droppednpp = [] #preprocesssing disabled

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
	prev_entries = len(datadf)
	datadf = datadf.replace('',np.NaN)
	datadf = datadf.dropna(axis=0, how='any')
	cur_entries = len(datadf)
	droppednpp.append(100-((100*cur_entries)/prev_entries)) 
	
	datadf["source"] = name	

	for key, entry in datadf.word1.items():
		#print(entry)
		if(entry == "sunrise"):
			print(str(datadf.source[key] + ": " + str(datadf.word2[key])))
	
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
		
		#also shuffle!
		
		#posts
		#posts = len(out['data'])
		#print(posts)		
		
		#print first 10 rows
		#print(out['data'].head(10))

		ppa.append(round(data.groupby(['word2'])['author'].transform('count').mean(),2))
		maxdup.append((data['word2'].value_counts()).max())
		meandup.append((data['word2'].value_counts()).mean())
		freqwords.append(data['word2'].value_counts().head(15))


		

	
	
