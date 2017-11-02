#Import the required libraries
import os
from showMenu import showMenu

class uInterface(object):
	def mainMenu(self, cfgData, clientSocket):
		while(True):
			self.cls() #Clear the previous menu before showing the new one
			showMenu().main() #Show the main menu items
			choice = input("Enter your menu choice: ")
			
			if choice == "2":
				self.objectMenu()
			elif choice == "3":
				self.transitMenu()
			elif choice == "5":
				self.TCPMenu(cfgData, clientSocket)
			elif choice == "6":
				self.locationMenu(cfgData)

	def locationMenu(self, cfgData):
		wrong_ch = False
		
		s_latlon = cfgData.getLatLon() #First element is latitude and second element is logitude
		s_alt = cfgData.getAltitude()
		
		while(True):
			loc_updt = cfgData.getUpdateStatus("location") #See if the location has been updated
			self.cls() #Clear the previous menu before showing the new one
			
			#Show current settings for the location
			print("****************************")
			if loc_updt == "yes":
				print("->Currently set location (updated):")
				cfgData.setUpdateStatus("location", "no")
			else:
				print("->Currently set location:")
			print("   [*]Latitude:  %s" %s_latlon[0] + u"\u00b0")
			print("   [*]Longitude: %s" %s_latlon[1] + u"\u00b0")
			print("   [*]Altitude:  %s" %s_alt + "m")
			print("****************************")
			
			showMenu().location()
			if wrong_ch:
				choice = input("Enter a correct number please: ")
			else:
				choice = input("Enter your menu choice: ")
			
			if choice == "1":
				self.cls() #Clear the screen for the new menu
				lat = self.getAngle("Latitude") #Get the latitude from the user
				lon = self.getAngle("Longitude") #Get the longitude from the user
				
				#Get the location's altitude
				print("\nEnter the location's altitude in meters.")
				alt = input("Altitude: ")
				
				#Print the values so the user sees a summary of what he entered
				print("\nThe values entered are:")
				print(" ->Latitude:  %s" %lat + u"\u00b0")
				print(" ->Longitude: %s" %lon + u"\u00b0")
				print(" ->Altitude:  %sm" %alt)
				
				#Ask if the values are accepted by the user
				acc = input("Do you accept the values? If yes type 'y', otherwise type anything: ")
				
				if acc == "y":
					#If the values entered are all the same with the already saved ones, do not update anything
					if (s_latlon[0] == lat) and (s_latlon[1] == lon) and (s_alt == alt):
						cfgData.setUpdateStatus("location", "no")
					else:
						s_latlon = [lat, lon]
						s_alt = alt
						cfgData.setLatLon(s_latlon)
						cfgData.setAltitude(s_alt)
					continue
			elif choice == "2":
				break
			else:
				wrong_ch = True

	def TCPMenu(self, cfgData, clientSocket):
		wrong_ch = False #Wrong choice indicator
		serv_change = False #Server change indicator
		
		#Read TCP settings from the XML configuration file
		s_host = cfgData.getHost()
		s_port = int(cfgData.getPort())
		s_autocon = cfgData.getTCPAutoConnStatus()
		
		while(True):
			print("Getting TCP connection status.")
			con_status = clientSocket.sendRequest("Test")
			self.cls() #Clear the previous menu before showing the new one
			
			#Show current settings for TCP
			print("****************************")
			print("->Current TCP settings:")
			print("   [*]Host: %s" %s_host)
			print("   [*]Port: %s" %s_port)
			if s_autocon == "yes":
				print("   [*]Autoconnect: Enabled")
			else:
				print("   [*]Autoconnect: Disabled")
			print("****************************")
			if con_status == "OK":
				print("->Connection status: Connected")
			else:
				print("->Connection status: Disconnected")
			print("****************************")
			
			showMenu().TCP() #Show the TCP menu choices
			if wrong_ch:
				choice = input("Enter a correct number please: ")
				wrong_ch = False
			else:
				choice = input("Enter your menu choice: ")
			
			#Control to be added
			if choice == "1":
				self.cls() #Clear the previous menu before showing the new one
				print("\nEnter the server host name e.g. \"localhost\" or 127.0.0.1:")
				host = input("Host: ") #Get the host name from the user
				print("The entered host is: " + host)
				#If statement to check if the entered host is the same as the saved one. If not change serv_change to True
				
				while(True):
					if wrong_ch:
						print("Please give an integer as the server port: ")
						wrong_ch = False
					else:
						print("\nNow enter the server port as an integer e.g. 10001: ")
					try:
						port = int(input("Port: "), 10) #Convert string from input to decimal integer
						break
					except:
						wrong_ch = True
						continue
				#If statement to check if the port and the host are the same as the saved ones. If they are not both the same change serv_change to True.
				#If both are the same, just return to the TCP menu.
				#First ask the user if the values entered are accepted and then move on.
				#If there are new values entered, and the user accepts them, inform the user that the current connection, if any, will be aborted,
				#And the values are going to be chaged.
				#Also ask the user if he wants a connection to be made with the new values.
				continue #Stay in the TCP menu
				
				#Add a ckeck first to see if the entered values are the same as the existing ones
				cfgData.setHost(host) #Save the host in the settings file
				cfgData.setPort(port) #Save the port in the settings file
			#Third choice to be added
			elif choice == "3":
				break
			elif choice == "4":
				break
			else:
				wrong_ch = True

	def transitMenu(self):
		self.cls() #Clear the previous menu before showing the new one
		showMenu().transit()
		choice = input("Enter your menu choice: ")
		
		#Control to be added
	
	def objectMenu(self):
		self.cls() #Clear the previous menu before showing the new one
		showMenu().object()
		choice = input("Enter your menu choice: ")
		
		#Control to be added
	
	def getAngle(self, angName):
		print("\nEnter the " + angName + " in decimal degrees.")
		print("For a south Latitude or a weste Longitude, enter a minus sign in the decimal value.")
		return input(angName + ": ") #Return the angle entered by the user
	
	def cls(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		showMenu().intro()


#Initial test code

#uInterface().mainMenu()