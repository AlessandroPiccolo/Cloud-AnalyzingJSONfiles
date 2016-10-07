from flask import Flask
from tasks import make_celery
import os
import swiftclient

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
	tweetRetrieve.delay()
	return "End flask route"

# Task that is beeing done by the celery workers
@celery.task(name= 'celery_ex.tweetRetrieve')
def tweetRetrieve():
	for data in conn.get_container(container_name)[1]:
		# data['name'] --> file name
		obj_tuple = conn.get_object(container_name, data['name'])
		with open(data['name'], 'w') as twitter_text:
			twitter_text.write(obj_tuple[1])
	return "End celery tweetRetrieve"		

if __name__ == '__main__':
	app.run(debug=True)
