"""
Created on Sun Jun 11 12:45:50 2017

@author: louweal

This script parses all scraped data into a clean dataset
"""


import json
import pandas as pd
import matplotlib as plt
#from pprint import pprint

data = []
for line in open('../learn-english/data/data_p1-p220.jl', 'r'):
	#print(line)
	data.append(json.loads(line))


datadf = pd.DataFrame(data)

#print first 10 rows
print(datadf.head(10))


#converts list ['word'] to string 'word' 
datadf['word'] = datadf['word'].apply(lambda x: ', '.join(x))

#print first 10 rows again
print(datadf.head(10))

# number of posts
posts = len(datadf)
print(posts)

#number of unique words
unique_posts = pd.Series(datadf['word'].value_counts())
num_unique_posts = len(unique_posts)
print(num_unique_posts)

#most common words
print(unique_posts.head(10))

#number of unique authors
unique_authors = pd.Series(datadf['author'].value_counts())
num_unique_authors = len(unique_authors)
print(num_unique_authors)

#average number of posts/author
print(round(posts/unique_authors,2))

#
#count_unique