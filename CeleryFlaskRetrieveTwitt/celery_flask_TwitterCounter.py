from flask import Flask
from tasks import make_celery
import os
import swiftclient
from collections import Counter
try:
	import json
except ImportError:
	import simplejson as json

# Containers name to retreive documents from
container_name 	= 'tweets'

# Setup connection to swift client containers
config = {'user':os.environ['OS_USERNAME'],
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}
conn = swiftclient.Connection(auth_version=3, **config)          

# Create flask app
app = Flask(__name__)
app.config['CELERY_BROKER_URL']='amqp://guest@localhost//'
app.config['CELERY_BACKEND']='rpc://'

# Create cellery worker
celery = make_celery(app)

# Method done by the flask app
@app.route('/twitterCount')
def process():
	tweetRetrieveAndCount.delay()

	return "End flask route\n"

# Task that is beeing done by the celery workers
@celery.task(name= 'celery_ex.tweetRetrieveAndCount')
def tweetRetrieveAndCount():
	# Words to count (pronomen in this case)	
	pronomen = {'han': 0, 'hon': 0, 'hen': 0, 
		    'den': 0, 'det': 0, 'denna': 0, 'denne': 0}

# Goes through each json file in container
# for data in conn.get_container(container_name)[1]:
# 	obj_tuple = conn.get_object(container_name, data['name'])

# Only check one json file in container	
	obj_tuple = conn.get_object(container_name, '05cb5036-2170-401b-947d-68f9191b21c6')

	# Download file (Can not figure out how to skip this step...)
	with open("temp", 'w') as twitter_text:
		twitter_text.write(obj_tuple[1])
	# Open temporary file and count pronomen	
	with open("temp", 'r') as twitter_text:
		for line in twitter_text:
			try:
				tweet = json.loads(line)
				if 'retweeted_status' not in tweet:
				# Basically dictionary, count of each word --> {'i': 2, 'am': 2}
					countsWord = Counter(tweet['text'].lower().split())
			 		for key in pronomen:
						if key in countsWord:
							pronomen[key] += countsWord[key]
			except:
				continue

	print(pronomen)
	# Create json file called result	
	with open("result", 'w') as result:
		result.write(json.dumps(pronomen, ensure_ascii=False))		
	
	return "End celery tweetRetrieve"

if __name__ == '__main__':
	app.run(debug=True)

