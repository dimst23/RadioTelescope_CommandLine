from User_Interface import uInterface
from configData import confData

if __name__ == '__main__':
	cfgData = confData("settings.xml")
	uInterface().mainMenu(cfgData)