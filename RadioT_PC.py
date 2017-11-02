#!/usr/local/bin/python

from User_Interface import uInterface
from configData import confData
import sys

if __name__ == '__main__':
	try:
		cfgData = confData("settings.xml")
	except Exception as e:
		print("There is a problem with the XML file handling.\n%s" %e)
		sys.exit(1) #Terminate the script
	
	#TCP exception handling code to be added for TCP too
	uInterface().mainMenu(cfgData)