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

## My scheme for the server requires it to listen for requests    ##
## on three ports, one for each required service, listed below:   ##
##                                                                ##
##    EDIT: Just listen for training data on port 80.             ##
##    port 24601 - receive data file from client(At last,         ##
##                 Valjean, we see each other plain!)             ##
##    port 42069 - send training file (pump out dank memes)       ##

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def SQLinsert(jsonthing):
    with open("dbcreds.conf") as conff:
        conflist = conff.read().splitlines()

    db = MySQLdb.connect(host = conflist[0], user = conflist[2], password = conflist[3], db = conflist[1])

    try:   
        with conn.cursor() as cur:
            cur.execute("INSERT INTO db training VALUES (%s)", jsonthing)
        conn.commit()
    finally:
        conn.close()

def gibeJSON():
    flat = flatten_json(request.json)
    SQLinsert(json_normalize(flat));    # MySQL
    
    # Write the file for training.
    timestamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    fname = timestamp + ".txt"
    with open(fname, "wb") as f:
        f.write(flat)
    
    return "success"
    
def servRun(servlogs):
    sendsock = S.socket(S.AF_INET, S.SOCK_STREAM)    # may use this for a service idk
    updatesock = S.socket(S.AF_INET, S.SOCK_STREAM)    # listen for message update requests
    grabsock = S.socket(S.AF_INET, S.SOCK_STREAM)    # listen for new files to send

    host = S.gethostname()           # grab this machine's name
    servlogs.write(host)
    grabsock.bind((host, 24601))     # bind host to socket to receive files from clients

    grabsock.listen(5)
    servlogs.write("##### START LISTENING #####")
    sendconn = -2    # flags for while loop below
    
    while True:    # continuously listen on all three ports
        ## Receive a file a user wants to send. ##
        timestamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        jsonfname = timestamp + ".json"
        fin = open(jsonfname, "wb")    # file we will create

        while sendconn == -2:
            sendconn, clientaddr = grabsock.accept()    # Now prepare to write the contents of an encrypted file!
            
            servlogs.write(strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + "    grabbing usage data from " + clientaddr)
            flag, i = "1", 0
            flag = sendconn.recv()   # If this flag is ever set to zero, the client is done sending files. 
            
            ## Now record the encrypted file the client user has sent. ##
            while(flag == "1"):
                fileContents = sencconn.recv()
                name = str(i) + "_.json"
                f = open(name, "wb")
                f.write(fileContents)
            
                ## SQL Insertion ##
                # SQLinsert(filecontents)
            
                f.close()
            
                i += 1
                flag = sendconn.recv()    # will send "1" if more files, "0" if no more
            
            sendconn.close()
            sendconn = -2
        grabsock.listen(5)
        servlogs.write(strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + "    Listening for recieve requests....")
        
def start():
    logstamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    logfile = logstamp + ".txt"
    servlogs = open(logfile, "wb")
    
    servRun(servlogs)
    servlogs.close()    # kill log reading if something goes wrong


if __name__ == '__main__':
    start()
