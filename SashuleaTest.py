#!/usr/bin/env python

import re
import os
import sys
import socket
import configparser as CP
import time #I tested with nc command and to see the answer we need a delay. 

def LogFileParser (string):
    try:
        f = open (cfg['DEFAULT']['LogFile'], 'r')
    except:
        print ('Can\'t open log file to analyze:', cfg['DEFAULT']['LogFile'])
        sys.exit(1)
    #here should be regular expression analyzer code, but as I don't have actual job to do, I'll hardcode return string as number of found lines
    linesFound = '14'
    return (linesFound)

def ReceivedDataStringCheck (string):
    #We need to check if the recieved string is what we need and wount brake our program or execute some code or worse!
    #The pattern string is unknown to me => answer is hardcoded
    CheckResult=True
    return(CheckResult)

#parsing config file and storing all data in mem. Reading it once on tcp listener start
cfg = CP.ConfigParser ()
#checking if file exists because configparser does not throw an error if there is no file
if not os.path.exists('SStest.conf'):
    print ('Can\'t find config file SStest.conf.')
    sys.exit(1)

try:
    os.path.exists('SStest.conf')
    cfg.read ('SStest.conf')
except CP.Error as msg:
    print ('Parsing config file failed. Error mesage: \n\r', msg)
    sys.exit(1)

#Now we should have all data. Trying to open a socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((cfg['DEFAULT']['Host'], int(cfg['DEFAULT']['Port'])))
except socket.error as msg:
    print ('Creating socket failed:\n\r', msg)
    sys.exit(1)

#If all is good so far, we wanna listen for a connection. We will use only one connection with default BUFFER size (1024) as we dont know the size of the recieved message;
try:
    while 1:
        s.listen(1)
        print ('Now waiting for connection... \r\nCtrl+C to exit')
        conn, addr = s.accept()
        print ('Connection established with ', addr)

        dataString = conn.recv(10000000)
        #print (dataString) #print receive message. Debug purpose
       # if not dataString: break
        if not ReceivedDataStringCheck(dataString):
            print ("Received string is not what we need. Sending answer")
            conn.send("Sorry, try again".encode())
            conn.close()
        else:
            answer = LogFileParser(dataString)
            print ('Sending answer: ', answer)
            conn.send(answer.encode())
            time.sleep(10) #just for nc purpose: $nc 127.0.0.1 15005 < ~/.bash_history
            conn.close()
except KeyboardInterrupt:
    s.settimeout(0.1)
    s.close()
    sys.exit(255)
