#!usr/bin/env python
########################################################################
# Stripped-down Snapchat Clone Server
# AUTHOR: Brandon Denton
#
# This script is intended to connect to a companion client application
# "picSwap.py" via a socket it creates to the server machine and send a
# file intended for that client through that socket. Right now, the 
# user has to define the file sent from the server by user input, but 
# eventually I'll have "server.py" search a directory on the host 
# machine made especially for the user currently connecting to it and 
# send that client files stored there.
########################################################################
#import logging as logs
import socket as S
import os    # We need to make a directory to store user keys and files to be sent.
from time import gmtime, strftime   # timestamping phone data files
import MySQLdb



## My scheme for the server requires it to listen for requests on three ports, ##
## one for each required service, listed below:                                ##
##                                                                             ##
##    port 24601 - login requests (At last, Valjean, we see each other plain!) ##
##    port 24602 - message update requests                                     ##
##    port 42069 - requests to send a file (listen 4 dank memes)               ##

#def SQLinsert(jsonthing):
#   conn = MySQLdb(host = "us", user = "", passwd = "", db = "")
#   obj = conn.cursor()
#   obj.execute("INSERT INTO db training VALUES (%s)", jsonthing)
#   conn.close()

def servRun():
    sendsock = S.socket(S.AF_INET, S.SOCK_STREAM)    # may use this for a service idk
    updatesock = S.socket(S.AF_INET, S.SOCK_STREAM)    # listen for message update requests
    grabsock = S.socket(S.AF_INET, S.SOCK_STREAM)    # listen for new files to send

    host = S.gethostname()           # grab this machine's name
    servlogs.write(host)
    grabsock.bind((host, 42069))     # bind host to socket to receive files from clients

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
                name = str(i) + "_"
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
