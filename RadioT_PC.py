#!/usr/local/bin/python

import User_Interface
import configData
import TCPClient
import logData
import sys

if __name__ == '__main__':
    #Exception handling section for the log file code
    try:
        logdata = logData.logData(__name__)
    except:
        print("There is a problem with the handling of the log file. See log file for the traceback of the exception.\n")
        logdata.log("EXCEPT", "There is a problem with the handling of the log file. Program terminates.", __name__)
        exit(1) #Terminate the script
    
    #Exception handling code for the XML file process
    try:
        cfgData = configData.confData("settings.xml")
    except:
        print("There is a problem with the XML file handling. See log file for the traceback of the exception.\n")
        logdata.log("EXCEPT", "There is a problem with the XML file handling. Program terminates.", __name__)
        exit(1) #Terminate the script
    
    #Exception handling code for the TCP initial setup
    try:
        tcpClient = TCPClient.TCPClient(cfgData)
    except:
        print("There is a problem with the TCP handling. See log file for the traceback of the exception.\n")
        logdata.log("EXCEPT", "There is a problem with the TCP handling. Program terminates.", __name__)
        exit(1) #Terminate the script
    
    #General exception handling code
    try:
        User_Interface.uInterface(cfgData, tcpClient) #Initiate the user interface
    except KeyboardInterrupt:
        print("User requested termination with a keyboard interrupt.\n")
        logdata.log("EXCEPT", "User requested termination with a keyboard interrupt.", __name__)
        exit(0) #Terminate the script
    except:
        print("Something really bad happened!! We should terminate.\n")
        logdata.log("EXCEPT", "Something really bad happened!! See the traceback below.", __name__)
        exit(1) #Terminate the script
    logdata.logClose() #Terminate all logging operations before exiting the script