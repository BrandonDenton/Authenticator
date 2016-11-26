#!usr/bin/env python3
########################################################################
# JSON-Receiving and Parsing TCP Server
# AUTHOR: Brandon Denton
#
# This script is intended to connect via TCP sockets to an Android 
# application which collects anonymiezed data about the usage of the 
# device on which it is running, read JSON objects sent along that 
# socket, and parse them appropriately for use by the MALLET topic
# modelling package
########################################################################
import socket as S
import os    # We need to make a directory to store user keys and files to be sent.
from time import gmtime, strftime   # timestamping phone data files
import MySQLdb
from flask import Flask, request
import json
import AuthHelper

## My scheme for the server requires it to listen for requests    ##
## on three ports, one for each required service, listed below:   ##
##                                                                ##
##    EDIT: Just listen for training data on port 80.             ##
##    port 24601 - receive data file from client(At last,         ##
##                 Valjean, we see each other plain!)             ##
##    port 42069 - send training file (pump out dank memes)       ##

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def start():
    logstamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    logfile = logstamp + ".txt"
    servlogs = open(logfile, "wb")
    
    gibeJSON()
    #servRun(servlogs)
    servlogs.close()    # kill log writing if something goes wrong

def gibeJSON():
    print(request)
    flat = flatten_json(request.json)
    SQLinsert(flat);    # MySQL
    
    # Write the file for training.
    timestamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    fname = timestamp + ".txt"
    with open(fname, "wb") as f:
        f.write(flat)
    os.system("mv fname ~/Desktop/Authenticator/training-data")    # We don't want MALLET to train on our logfiles. :0

    # Format the text file properly and build topic models.
    os.system("bin/mallet import-dir --input ~/Desktop/Authenticator/training-data --output topic-input.mallet \
  --keep-sequence --remove-stopwords")
    os.system("bin/mallet train-topics --input topic-input.mallet \
  --num-topics 100 --output-state topic-state.gz")
    
    # cleanup
    os.system("rm topic-input.mallet")

    return "success"


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True, host='0.0.0.0', port=42069)
