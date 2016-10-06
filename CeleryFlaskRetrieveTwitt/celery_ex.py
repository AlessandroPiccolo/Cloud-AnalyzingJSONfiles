from flask import Flask
from tasks import make_celery
import os
import swiftclient
try:
	import json
except ImportError:
	import simplejson as json

# Containers name to retreive documents from (do not forget to source g.. first)
container_name = 'tweets'

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
	# Words to count (pronomen in this case)	
	pronomen = [['han',0], ['hon',0], ['hen',0], ['den',0], ['det',0], ['denna',0], ['denne',0]]
	# Go through each json file in container
	for data in conn.get_container(container_name)[1]:
		# data['name'] --> file name
		obj_tuple = conn.get_object(container_name, data['name'])		
		# Count each pronomen inside json file, print inside new json
		# Name of file data['name']		
		with open(data['name'], 'r') as twitter_text:
			 
			#twitter_text.write(obj_tuple[1]) # Downloads json file on machine			
			for line in twitter_text: #obj_tuple[1]:
				for word[0] in pronomen:
					if(word in line['text'] and ('RT' not in line['text'])):
						word[1]+=1			
	return "End celery tweetRetrieve"

if __name__ == '__main__':
	app.run(debug=True)
