#!/usr/local/bin/python

from User_Interface import uInterface
from configData import confData
from TCPClient import TCPClient
import sys

if __name__ == '__main__':
	try:
		cfgData = confData("settings.xml")
	except Exception as e:
		print("There is a problem with the XML file handling.\n%s" %e)
		sys.exit(1) #Terminate the script
	
	try:
		tcpClient = TCPClient(cfgData)
	except Exception as e:
		print("There is a problem with the TCP handling.\n%s" %e)
		sys.exit(1) #Terminate the script
	uInterface().mainMenu(cfgData, tcpClient)