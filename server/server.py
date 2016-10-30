#!usr/bin/env python
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
#import pymysql.cursors


## My scheme for the server requires it to listen for requests on three ports, ##
## one for each required service, listed below:                                ##
##                                                                             ##
##    port 24601 - receive training file (At last, Valjean, we see each other plain!) ##
##    port 24602 - message update requests                                     ##
##    port 42069 - send training file (pump out dank memes)               ##

#def SQLinsert(jsonthing):
#   conn = pymysql.connect(host = "us", user = "", password = "", db = "")
#
#   try:   
#       with conn.cursor() as cur:
#           cur.execute("INSERT INTO db training VALUES (%s)", jsonthing)
#       conn.commit()
#   finally:
#       conn.close()

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
