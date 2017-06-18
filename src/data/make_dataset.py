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
	"bleeping_computer":"../../data/raw/bleeping_computer.jl",
	"ecig":"../../data/raw/ecig.jl",
	"gog":"../../data/raw/gog.jl",
	"learn_english":"../../data/raw/learn-english.jl",
	"pinkbike":"../../data/raw/pinkbike.jl",
	"sas":"../../data/raw/sas.jl",
	"the_fishy":"../../data/raw/the_fishy.jl",
	"wrongplanet":"../../data/raw/wrongplanet.jl"
}

def preprocess(x):
	x = x.lstrip('"') # todo
	x = x.lstrip(' ')
	x = x.split("Quote:")[0] # removes posts containing quotes from SAS
	x = x.split("(")[0]
	x = x.split(",")[0]
	x = x.split("*")[0]
	x = x.split("--")[0]	
	x = x.split("*")[0]
	x = x.split('"')[0]	
	x = x.split(".")[0]		
	x = x.split("!")[0]		
	x = x.split("?")[0]
	x = x.split("=")[0]
	x = x.split("[")[0]		
	x = x.split(":")[0]		
	x = x.split(";")[0]
	x = x.split("Edited by")[0] # bleeping_computer: additional post info was scraped		
	#x = x.split(" - ")[0]		
	x = x.rstrip('\u00a0') # removes trailing non-breaking spaces 
	x = x.rstrip(' ')

	return x

nans = []

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

	# add source name
	datadf["source"] = name	
	#convert usernames to IDs
	datadf['author'] = datadf['author'].astype('category')
	datadf['author'] = datadf['author'].cat.codes	
	#combine id with source (e.g. wrongplanet10)
	datadf['author'] = datadf["source"] + datadf["author"].map(str)
	datadf['author'] = datadf['author']
	
	#converts list ['word'] to string 'word' 
	if(name != "bleeping_computer" and name != "sas"):
		datadf['word'] = datadf['word'].apply(lambda x: ', '.join(x))

	# ...
	datadf['word'] = datadf['word'].apply(lambda x: preprocess(x))	
	#convert all to lowercase
	#datadf['word'] = datadf['word'].apply(lambda x: x.lower())

	#create pair with current word and previous word
	datadf['word1'] = datadf['word'].shift(1)	
	# rename column 'word' to 'word2'
	datadf.rename(columns={'word' : 'word2'}, inplace=True)

	#replace all empty words with NaN	
	datadf = datadf.replace('',np.NaN)

	# compute fraction NaN values
	nans.append(100*(datadf['word2'].isnull().sum())/len(datadf)) 

	# drop all pairs containing NaN	values
	datadf = datadf.dropna(axis=0, how='any').reset_index(drop=True)

	

	for key, entry in datadf.word1.items():
		#print(entry)
		if(entry == "sunrise"):
			print(str(datadf.source[key] + ": " + str(datadf.word2[key])))
	
	#rearrange columns
	cols = ['author','word1','word2','source']
	datadf = datadf[cols]
	temp['data'] = datadf	
	return temp


out_data = pd.DataFrame()
ppa = []
maxdup = []
meandup = []
freqwords = []
sample = []
out = pd.DataFrame()

#parse sources in alphabetical order
for key, value in iter(sorted(sources.items())): 
	if(key == key):
		print("Parsing " +str(key) + "...")
		out = parse(key, value)
		data = out['data']

		out_data = out_data.append(data, ignore_index=True)
		


		ppa.append(round(data.groupby(['word2'])['author'].transform('count').median(),2))
		maxdup.append((data['word2'].value_counts()).max())
		meandup.append((data['word2'].value_counts()).mean())
		freqwords.append(data['word2'].value_counts().head(30))
		sample.append(data['word2'].sample(15))


		
#convert author IDs (e.g. wrongplanet10) to unique integer IDs
out_data['author'] = out_data['author'].astype('category')
out_data['author'] = out_data['author'].cat.codes		



print(out_data.sample(15))

#shuffle all rows
out_data = out_data.sample(frac=1).reset_index(drop=True)

#write to csv
out_data.to_csv('../../data/processed/wordgame.csv', sep=',')	
