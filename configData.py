import xml.etree.ElementTree as etree
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import os

class confData(object):
	#Class construcor
	def __init__(self, filename):
		self.filename = filename #Create a variable with the given filename
		self.parse() #Parse the XML file
	
	def parse(self):
		self.tree = etree.parse(self.filename)
		self.root = self.tree.getroot()
		
	def getConfig(self, child, subchild):
		#self.parse()
		children = list(self.root.find(child))
		for item in children:
			if item.tag == subchild:
				return item.text
			else:
				continue
	
	def getLatLon(self):
		lat = self.getConfig("location", "latitude")
		lon = self.getConfig("location", "longitude")
		return [lat, lon]
	
	def getHost(self):
		host = self.getConfig("TCP","host")
		return host
	
	def getPort(self):
		port = self.getConfig("TCP","port")
		return port
	
	def getTCPAutoStart(self):
		start = self.getConfig("TCP","autoconnect")
		return start