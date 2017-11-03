#!/usr/local/bin/python

from User_Interface import uInterface
from configData import confData
from TCPClient import TCPClient
import sys

if __name__ == '__main__':
    #Exception handling code for the XML file proccess
    try:
        cfgData = confData("settings.xml")
    except Exception as e:
        print("There is a problem with the XML file handling.\n%s" %e)
        sys.exit(1) #Terminate the script
    
    #Exception handling code for the TCP initial setup
    try:
        tcpClient = TCPClient(cfgData)
    except Exception as e:
        print("There is a problem with the TCP handling.\n%s" %e)
        sys.exit(1) #Terminate the script
    
    #General exception handling code
    try:
        uInterface(cfgData, tcpClient) #Initiate the user interface
    except Exception as e:
        print("Something really bad happened!! We should terminate.\n%s" %e)