
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


