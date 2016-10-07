import os
try:
	import json
except ImportError:
	import simplejson as json


from collections import Counter


#remove
count = 0

pronomen = {'han': 0, 'hon':0, 'hen':0, 'den':0, 'det':0, 'denna':0, 'denne':0}
	
with open('temp (copy)', 'r') as twitter_text: 	
	for line in twitter_text:
		try:
			tweet = json.loads(line)
			print(tweet['text'])
			if 'retweeted_status' not in tweet:
				# Basically dictionary, count of each word --> {'i': 2, 'am': 2}
				countsWord = Counter(tweet['text'].lower().split())
			 	for key in pronomen:
					if key in countsWord:
						pronomen[key] += countsWord[key]
		except:
			continue	
 
print(pronomen)
