from flask import Flask
from tasks import make_celery
import os
import swiftclient
try:
	import json
except ImportError:
	import simplejson as json

# Containers name to retreive documents from
container_name 	= 'tweets'
# Words to count (pronomen in this case)	
pronomen 		= ['han', 'hon', 'hen', 'den', 'det', 'denna', 'denne']
pronomenCounter = [0]*len(pronomen)
# Total count of pronomens
count 			= 0 

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
@app.route('/process')
def process():
	tweetRetrieveAndCount.delay()
	return "End flask route"

# Task that is beeing done by the celery workers
@celery.task(name= 'celery_ex.tweetRetrieveAndCount')
def tweetRetrieveAndCount():
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
				for i in range(len(pronomen)):
					if(pronomen[i] in tweet['text'] and ('RT' not in tweet['text'])):
						pronomenCounter[i] += 1	
						count += 1	
			except:
				continue
#	for contr in pronomenCounter:
#		print(contr)
	return "End celery tweetRetrieve count = " + str(count)

if __name__ == '__main__':
	app.run(debug=True)
