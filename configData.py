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
				self.tree.write(self.filename)
				break
			else:
				continue
	
	def getUpdateStatus(self, element):
		return self.root.find(element).get("updated")
	
	def setUpdateStatus(self, element, status):
		self.root.find(element).set("updated", status)
		self.tree.write(self.filename)
	
	def getLatLon(self):
		lat = self.getConfig("location", "latitude")
		lon = self.getConfig("location", "longitude")
		return [lat, lon]
		
	def setLatLon(self, location):
		self.setConfig("location", "latitude", location[0])
		self.setConfig("location", "longitude", location[1])
	
	def getAltitude(self):
		return self.getConfig("location", "altitude")
	
	def setAltitude(self, altitude):
		self.setConfig("location", "altitude", altitude)
	
	def getHost(self):
		return self.getConfig("TCP", "host")
		
	def setHost(self, host):
		self.setConfig("TCP", "host", host)
	
	def getPort(self):
		return self.getConfig("TCP", "port")
		
	def setPort(self, port):
		self.setConfig("TCP", "port", port)
	
	def getTCPAutoStart(self):
		return self.getConfig("TCP", "autoconnect")
		
	def setTCPAutoStart(self, strt):
		self.setConfig("TCP", "autoconnect", strt)