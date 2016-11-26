#!usr/bin/env python
import MySQLdb
import json

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
    print("Connecting to database....")
    with open("dbcreds.conf") as conff:
        conflist = conff.read().splitlines()

    db = MySQLdb.connect(host = conflist[0], user = conflist[2], passwd = conflist[3], db = conflist[1])

    try:   
        with conn.cursor() as cur:
            cur.execute("INSERT INTO db training VALUES (%s)", jsonthing)
        conn.commit()
    finally:
        conn.close()
