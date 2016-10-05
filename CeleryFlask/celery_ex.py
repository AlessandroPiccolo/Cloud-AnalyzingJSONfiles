from flask import Flask
from tasks import make_celery
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL']='amqp://guest@localhost//'
app.config['CELERY_BACKEND']='rpc://'

celery = make_celery(app)

@app.route('/process/<name>')
def process(name):
	reverse.delay(name)  # celery task
	return 'I sent an async request!' #name #"Hope fully file names"

@celery.task(name= 'celery_ex.reverse')
def reverse(string):
	return string[::-1]

if __name__ == '__main__':
	app.run(debug=True)
