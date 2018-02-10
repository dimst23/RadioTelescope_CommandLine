#!/usr/local/bin/python

import User_Interface
import configData
import TCPClient
import logData
import sys

if __name__ == '__main__':
    logdata = logData.logData(__name__)
    
    #Exception handling code for the XML file process
    try:
        cfgData = configData.confData("settings.xml")
    except Exception as e:
        print("There is a problem with the XML file handling.\n%s" %e)
        logdata.log("EXCEPT", "There is a problem with the XML file handling. Program terminates.", __name__)
        exit(1) #Terminate the script
    
    #Exception handling code for the TCP initial setup
    try:
        tcpClient = TCPClient.TCPClient(cfgData)
    except Exception as e:
        print("There is a problem with the TCP handling.\n%s" %e)
        logdata.log("EXCEPT", "There is a problem with the TCP handling. Program terminates.", __name__)
        exit(1) #Terminate the script
    
    #General exception handling code
    try:
        User_Interface.uInterface(cfgData, tcpClient) #Initiate the user interface
    except:
        print("Something really bad happened!! We should terminate.\n")
        logdata.log("EXCEPT", "Something really bad happened!! See the traceback below.", __name__)
        exit(1) #Terminate the script
    logdata.logClose()