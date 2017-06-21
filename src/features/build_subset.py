"""
Created on Sun Jun 11 12:45:50 2017

@author: louweal

This script writes a subset of the data to a file
"""
import pandas as pd

#read input data
infile = pd.read_csv('../../data/processed/wordgame_201706.csv')

#create new dataframe
df = pd.DataFrame(infile)

# select rows based on word1
subset = df[df['word1'] == "music"]

#set output filename
outfile = "../../data/processed/music.csv"

# write rows to file
subset.to_csv(outfile, index=False)
