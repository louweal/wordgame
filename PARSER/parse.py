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
	"gog":"../gog/data/data_p1-p5054.jl",
	"pinkbike":"../pinkbike/data/data_p1-p2747.jl",
	"wrongplanet":"../wrongplanet/data/data_p1-p3825.jl", 
	"aspiecentral":"../aspiecentral/data/data_p1-p1152.jl",
	"learn_english":"../learn-english/data/data_p1-p220.jl"
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
	#x = x.split(" - ")[0]		
	x = x.rstrip(' ')
	x = x.lstrip(' ')
	return x

def parse(name, scraped_data):
	temp = {}

	data = []
	for line in open(scraped_data, 'r'):
		#print(line)
		data.append(json.loads(line))
	
	# convert data to pandas Dataframe
	datadf = pd.DataFrame(data)
	
	#remove first post in topic
	datadf = datadf.ix[1:] 	
	
	#converts list ['word'] to string 'word' 
	datadf['word'] = datadf['word'].apply(lambda x: ', '.join(x))

	#convert all to lowercase
	datadf['word'] = datadf['word'].apply(lambda x: x.lower())
	datadf['word'] = datadf['word'].apply(lambda x: preprocess(x))	

	datadf['word1'] = datadf['word'].shift(1)	
	datadf['word2'] = datadf['word']
	datadf = datadf.drop('word', 1)



	
	# drop empty posts '' (row ids remain) [better method?]
	datadf = datadf.replace('',np.NaN)
	datadf = datadf.dropna(axis=0, how='any')
	
	#number of unique words
	temp['words'] = pd.Series(datadf['word2'].value_counts())
	
	#number of unique authors
	temp['authors'] = pd.Series(datadf['author'].value_counts())
	
	datadf["source"] = name	
	
	temp['data'] = datadf	
	return temp


#struct to contain all features from dataset
#earn_english = parse('../learn-english/data/data_p1-p220.jl')
#aspiecentral = parse('../aspiecentral/data/data_p1-p1152.jl')
wrongplanet = parse('wrongplanet', '../wrongplanet/data/data_p1-p3825.jl')

for key, value in sources.items():
	if(key == "pinkbike"):
		out = parse(key, value)

		#posts
		posts = len(out['data'])
		print(posts)		
		
		#print first 10 rows
		print(out['data'].head(10))
		
		
		#most common words
		print(out['words'].head(25))
		
		
		#unique words
		words = len(out['words'])
		print(words)
	
	
	
