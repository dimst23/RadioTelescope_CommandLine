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
		#Add a handling code for the case parsing fails
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
	
	def setConfig(self, element, child, value):
		elm = self.root.find(element) #Get the required element from the tree
		children = list(elm) #List the children of the element
		for item in children:
			if item.tag == child:
				item.text = value
				elm.set("updated", "yes")
				self.tree.write("settings.xml")
				break
			else:
				continue
	
	def getUpdateStatus(self, element):
		return self.root.find(element).get("updated")
	
	def setUpdateStatus(self, element, status):
		self.root.find(element).set("updated", status)
		self.tree.write("settings.xml")
	
	def getLatLon(self):
		lat = self.getConfig("location", "latitude")
		lon = self.getConfig("location", "longitude")
		return [lat, lon]
	
	def getAltitude(self):
		return self.getConfig("location", "altitude")
	
	def getHost(self):
		return self.getConfig("TCP", "host")
	
	def getPort(self):
		return self.getConfig("TCP", "port")
	
	def getTCPAutoStart(self):
		return self.getConfig("TCP", "autoconnect")