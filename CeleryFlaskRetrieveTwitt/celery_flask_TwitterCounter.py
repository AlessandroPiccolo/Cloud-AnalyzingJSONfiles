from __future__ import division
from flask import Flask, render_template
from tasks import make_celery
import os
import sys
import swiftclient
import pygal
import ast
import StringIO
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

################# Flask Methods #################

# Request celery to count pronomen in tweets
@app.route('/twitterCount', methods=["GET"])
def twitterCount():
	tweetRetrieveAndCount.delay()
	return "Requesting celery to count pronomen in twitter feed\n"

# Creates bar graph out of json file
@app.route('/vis', methods=["GET"])
def vis():
        if os.path.isfile("result"):
		bar_chart = pygal.Pie() # Make pie chart in pygal
		with open("result", 'r') as result_json:
			try:
				result_dict = ast.literal_eval(result_json.read())
				total_count  = sum(result_dict.values())
				# Add actual data for making graph
				for key in result_dict:
					bar_chart.add(key, [(result_dict[key]/total_count)*100])
			except Exception, e:
				return(str(e))
		# Giving the chart (pygal object) info
		bar_chart.y_title = "Relative usage of pronomen in tweets [%]"
		bar_chart.title = "Usage of different pronumens in tweets"
		bar_chart_data = bar_chart.render_data_uri()
		return render_template("graphing.html", bar_chart_data = bar_chart_data)
	else:
        	return "No result present, run twitter count\n"

################# Celery Methods #################

# Task that is beeing done by the celery worker
@celery.task(name= 'celery_ex.tweetRetrieveAndCount')
def tweetRetrieveAndCount():
	# Words to count (pronomen in this case)
	pronomen = {'han': 0, 'hon': 0, 'hen': 0,
		    'den': 0, 'det': 0, 'denna': 0, 'denne': 0}
	#amount_files_to_use = 5 # Number of json files to use in count
	#counter_temp = 0;
	# Goes through each json file in container
	for data in conn.get_container(container_name)[1]:
		#counter_temp +=1
		#if counter_temp == amount_files_to_use:
		#	break
 		obj_tuple = conn.get_object(container_name, data['name'])
		currentLine = 0
		# Splitlines --> returns list of lines, each {} becomes an element
		# [json object, "/n", json obj, "/n" ... ]
		for line in obj_tuple[1].splitlines():
			currentLine += 1
			if currentLine % 2 == 0:
				continue # Jump to next iteration, skip odd empty lines
			try:
				tweet = json.loads(line) # Tweet is dictionary now
				if 'retweeted_status' not in tweet: # Only unique tweets!
					# Basically dictionary, count of each word --> {'i': 2, 'am': 2}
					countsWord = Counter(tweet['text'].lower().split())
					for key in pronomen:
						if key in countsWord: # Find pronomen in tweets
							pronomen[key] += countsWord[key]
			except ValueError:
				print(ValueError)
			except:
				continue
	print(pronomen)
	# Create json file called result
	with open("result", 'w') as result:
		json.dump(pronomen, result)
	return "End celery tweetRetrieve"

if __name__ == '__main__':
	app.run(host = "0.0.0.0", debug=True)

