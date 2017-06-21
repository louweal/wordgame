"""
Created on Sun Jun 11 12:45:50 2017

@author: louweal

This script parses all scraped data into a clean dataset
"""

import json
import pandas as pd
import numpy as np
import matplotlib as plt
import re
#from pprint import pprint

sources = { #sources in alphabetical order 
	"aspiecentral":"../../data/raw/aspiecentral.jl",
	"atu2":"../../data/raw/atu2.jl",
	"classic_comics":"../../data/raw/classic_comics.jl",
	"bleeping_computer":"../../data/raw/bleeping_computer.jl",
	"ecig":"../../data/raw/ecig.jl",
	"gog":"../../data/raw/gog.jl",
	"learn_english":"../../data/raw/learn-english.jl",
#	"pinkbike":"../../data/raw/pinkbike.jl", # extremely messy data! (e.g. mainly posts about boobs, sex, insults etc.)
	"sas":"../../data/raw/sas.jl",
	"the_fishy":"../../data/raw/the_fishy.jl",
	"wrongplanet":"../../data/raw/wrongplanet.jl"
}

def preprocess(x):
	#replace..
	x = x.replace('\n',' ') # (wrongplanet)
	x = x.replace('_','')
	x = x.replace("`", "'")
	x = x.replace("~", "")
	x = x.replace("^", "")
	x = re.sub("xd", "", x, flags=re.I) # removes xD/XD/xd etc.. 
	

	#remove everything following...
	x = x.split("Quote:")[0] # removes posts containing quotes from SAS
	x = x.split("Sent from my")[0] # removes mobile Tapatalk message (SAS)
	x = x.split("Edited by")[0] # bleeping_computer: additional post info was scraped
	x = x.split("Posted via")[0] #sas
	if(x.find("said:") > 1): x = '' #classic comics: removes posts containing quotes
	x = x.split("\t")[0] 
	x = x.split("/")[0]		
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
	x = x.split("{")[0]		
	x = x.split(":")[0]		
	x = x.split(";")[0]
	x = x.split(" - ")[0]
	x = x.split(">")[0]
	x = x.split("<")[0] # deals with <comments> and <333 

	#remove leading characters
	x = x.lstrip(' ')
	x = x.lstrip("'")

	#remove trailing characters		
	x = x.rstrip('\u00a0') # removes trailing non-breaking spaces 
	x = x.rstrip('-M') # crazy 'signature' of a person with a lot of posts..
	x = x.rstrip('-m')
	x = x.rstrip("'")
	x = x.rstrip(' ')
	return x

nans = []
pps = [] #post/source

def parse(source_name, file):
	raw_data = []
	for line in open(file, 'r'):
		#print(line)
		raw_data.append(json.loads(line))
	
	# convert data to pandas Dataframe
	interm_data = pd.DataFrame(raw_data)
	
	#remove first post in topic
	interm_data = interm_data.ix[1:] 	

	# add source name
	interm_data["source"] = source_name	
	
	#convert usernames to IDs
	interm_data['author'] = interm_data['author'].astype('category')
	interm_data['author'] = interm_data['author'].cat.codes	
	#combine id with source (e.g. wrongplanet10)
	interm_data['author'] = interm_data["source"] + interm_data["author"].map(str)
	interm_data['author'] = interm_data['author']
	
	#if each post is scraped as a list of words
	if((source_name != "bleeping_computer") and (source_name != "classic_comics") and (source_name != "sas")):
		#converts lists ['word'] to string 'word'  
		interm_data['word'] = interm_data['word'].apply(lambda x: ', '.join(x))

	# clean data
	interm_data['word'] = interm_data['word'].apply(lambda x: preprocess(x))	

	#convert all to lowercase
	#interm_data['word'] = interm_data['word'].apply(lambda x: x.lower())

	#create pair with current word and previous word
	interm_data['word1'] = interm_data['word'].shift(1)	
	# rename column 'word' to 'word2'
	interm_data.rename(columns={'word' : 'word2'}, inplace=True)

	#replace all empty words with NaN	
	interm_data = interm_data.replace('',np.NaN)

	# compute fraction NaN values
	nans = 100*(interm_data['word2'].isnull().sum())/len(interm_data)

	# drop all pairs containing NaN	values
	interm_data = interm_data.dropna(axis=0, how='any').reset_index(drop=True)
	print("\tdropped pairs: " +str(round(nans,1)) + str("%"))	
	
	#rearrange columns
	cols = ['author','word1','word2','source']
	interm_data = interm_data[cols]

	return interm_data


processed_data = pd.DataFrame()

#parse sources in alphabetical order
for key, value in iter(sorted(sources.items())): 
	print("Parsing " +str(key) + "...")
	interm_data = parse(key, value)
	processed_data = processed_data.append(interm_data, ignore_index=True)
		
print("Finished parsing all data...")
		
#convert author IDs (e.g. wrongplanet10) to unique integer IDs
print("Creating anonymous user IDs...")
processed_data['author'] = processed_data['author'].astype('category')
processed_data['author'] = processed_data['author'].cat.codes		

#shuffle all rows
processed_data = processed_data.sample(frac=1).reset_index(drop=True)


#write to csv
outfile = "../../data/processed/wordgame_201706.csv"
print("Writing data to " + str(outfile) + "...")
processed_data.to_csv(outfile, sep=',', index=False)	

