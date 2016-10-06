import os
try:
	import json
except ImportError:
	import simplejson as json

#remove
count = 0

pronomen = ['han', 'hon', 'hen', 'den', 'det', 'denna', 'denne']
pronomenCounter = [0]*len(pronomen)
	
with open('05cb5036-2170-401b-947d-68f9191b21c6', 'r') as twitter_text: 	
	for line in twitter_text:
		try:
			tweet = json.loads(line)
			for i in range(len(pronomen)):
				#print(str(pronomen[i]))
				if(pronomen[i] in tweet['text'] and ('RT' not in tweet['text'])):
					pronomenCounter[i] += 1	
					count += 1	
		except:
			continue	

print('number of word counted ' + str(count))

for count in pronomenCounter:
	print(count)
