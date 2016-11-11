#!usr/bin/env python
import socket
import sys
import numpy

## Read comms config file.
confarr = []
with open("commConf.txt", "rb") as conff:
    for line in conff:
        line = line.replace("\n","")
        confarr.append(line)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (confarr[0], int(confarr[1]))
print("connecting to " + confarr[0] + "port " + confarr[1] + "\n")
sock.connect(server_address)

try:
    message = 'This is the message.  It will be repeated.'
    print("sending " + message)
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print("received " + data)
except:
    print("whoops, couldn't connect. :'(")


finally:
    print("closing socket")
    sock.close()
