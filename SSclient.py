#!/usr/bin/env python

import os, sys, re, socket
import configparser as CP

def inputStringChecker (string):
    #I thing it would be a good idea to check the string on client side too.
    #Anyway, I dunno what to check.
    string = string.encode()
    return (string)

#generally, one would like to have separate config for a client with just an Host and Port to connect to, but as for test purpose, we use one machine and we can use the same file
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

#now we should get an input string to send 
try:
    print ('Please provide an input string to send to server or CTRL+C to exit:')
    inputString = input ()
    inputString = inputStringChecker(inputString)
except KeyboardInterrupt:
    print ('\r\nExiting...')
    sys.exit(255)
except:
    print ('String input failed. Exiting')
    sys.exit(1)

#Now we open a connection to the server...
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cfg['DEFAULT']['Host'], int(cfg['DEFAULT']['Port'])))
    s.send(inputString)
    answer = s.recv(1000000)
    print ('Server returned: ', str(answer.decode()))
except socket.error as msg:
    print ('Creating socket failed:\n\r', msg)
    sys.exit(1)

