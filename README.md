# Cloud computing - Analyse twitter Json files
In this assignment, you will build a prototype system to analyze a dataset of Twitter tweets collected beforehand using Twitter’s datastream API. The tweets are available in the public container ‘tweets’ in the SSC cloud, and the dataset consists of a number of files containing lineseparated tweet entries. Every second line is a blank line.

Count pronomen from unique tweets in JSON file using celery, rabbit and flask. Basically it uses flask api to request a celery worker to count pronomen in json files containing tweets from a private swift container. It outputs a json file with the count, ex

results: <br />
{"han": 1757, "hon": 385, "det": 997, "denne": 11, "den": 2287, "denna": 42, "hen": 31}

A json file downloaded from the swift container looks like the "tweets" file.

## How to use on Ubuntu16
All the neccesary files are in labb3/CeleryFlaskRetrieveTwitt/ <br />
Open 2 terminals and ssh to instance, source g2015034-openrc.sh to each <br />
terminal 1: celery -A celery_flask_TwitterCounter.celery worker --loglevel=info <br />
terminal 2: python celery_flask_TwitterCounter.py <br />

Open webpage from any computer do  <br />
http://floatingip:port/vis 		       (gives visualization if result file there) <br />
http://floatingip:port/twitterCount  (gives request to celery) <br />

## Need to install Ubuntu16
sudo apt-get update<br />
sudo apt-get upgrade<br />
sudo apt-get install rabbitmq-server<br />
sudo locale-gen sv_SE.UTF-8<br />
sudo apt-get install python-pip<br />
sudo pip install celery<br />
sudo apt install python-celery-common<br />
sudo pip install flask <br />
sudo pip install python-swiftclient<br />
sudo apt-get install python-keystoneclient<br />
sudo pip install pygal<br />
