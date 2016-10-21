Entity Extraction Service
======================

Named Entity Recognition. Uses a dictionary for phrases to be considered entities.
Those phrases has been from DBpedia some time ago. A final user can add its own.

A docker image with this modules as it is here is available at https://hub.docker.com/r/mixedemotions/08_entity_extraction_pt/

Installation
------------

Python 3 is necessary to run the service. Required libraries are:
* tornado

Starting and stopping the service
---------------------------------

There is a script that starts and stops the service with the desired configuration:

	./launcher.sh start
	./launcher.sh stop

This same script contains the configuration for running the service with a given
number of separated processes, using the port range as defined.

Configuring the service
-----------------------

The service needs a set of entities with inlinks in the data/pagelinlks_all.tsv file.
In that file, each line is an entry consisting on a phrase to be detected and an inlink number, which is the number of articles pointing to that entity.

Additionaly, the inlinks threshold must be set in the conf.py file as INLINKS_THRESHOLD. The default value is 400. Entities with a inlinks count below inlinks threshold will be ignored.

Calling the service
-------------------

This service admits both GET and POST requests.

### Calling the service via GET

An example call would be:

	http://[ip_address]:[port]/?text=EEUU%20cierra%20la%20investigación%20sobre%20las%20torturas%20de%20la%20CIA%20sin%20acusados


The inlinks_threshold can also be set in the query.

	http://[ip_address]:[port]/?inlinks_threshold=100&text=EEUU%20cierra%20la%20investigación%20sobre%20las%20torturas%20de%20la%20CIA%20sin%20acusados

This call returns a JSON object with the elapsed time, the detected entities and
some additional information.

The response is a json map. E.g.:

    {
      concepts: [
        "cristiano ronaldo",
        "messi"
      ]
    }

### Calling the service via POST

The POST expects a text per line.

The response is a json with an item per entry in the body.


    {
      "response": [
        {
          "text": "alguien como Einstein\r",
          "concepts": []
        },
        {
          "text": "nada por aquí\r",
          "concepts": []
        },
        {
          "text": "otra frase",
          "concepts": []
        }
      ]
    }

Creating a Docker Image
-----------------------
For creating a docker image, just configure your own data files (pagelinks_all.tsv and stopwords.txt) and set up an INLINKS_THRESHOLD in conf.py.
Then execute:

    docker build -t {name} .



