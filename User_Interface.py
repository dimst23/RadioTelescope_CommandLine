#Import the required libraries
import os

class uInterface(object):
	def intro(self):
		print("***********************************************")
		print("**  A.U.Th Radio Telescope Control Software  **")
		print("**                                           **")
		print("**  by Dimitrios Stoupis - dstoupis@auth.gr  **")
		print("***********************************************")
	
	def mainMenu(self):
		while(True):
			self.cls() #Clear the previous menu before showing the new one
			print("Main Menu:")
			print("1. Read Position")
			print("2. Choose object")
			print("3. Transit")
			print("4. Aim and guide")
			print("5. TCP settings")
			print("6. Location settings")
			choice = input("Enter your menu choice: ")
			
			if choice == "2":
				self.objectMenu()
			elif choice == "3":
				self.transitMenu()
			elif choice == "5":
				self.TCPMenu()
			elif choice == "6":
				self.locationMenu()

	def locationMenu(self):
		wrong_ch = False
		while(True):
			self.cls() #Clear the previous menu before showing the new one
			#Show current settings on the top. That will be done latter after deciding for the final menu outline
			print("Location Menu:")
			print("1. Set new location")
			print("2. Return to main menu")
			if wrong_ch:
				choice = input("Enter a correct number please: ")
			else:
				choice = input("Enter your menu choice: ")
			
			#Control to be added
			if choice == "1":
				self.cls() #Clear the screen for the new menu
				lat = self.setAngle("Latitude")
				print("Latitude is set to: " + lat)
				lon = self.setAngle("Longitude")
				print("Longitude is set to: " + lon)
				acc = input("Do you accept the values? If yes type 'y', otherwise type anything: ")
				if acc == "y":
					break
			elif choice == "2":
				break
			else:
				wrong_ch = True

	def TCPMenu(self):
		wrong_ch = False
		while(True):
			self.cls() #Clear the previous menu before showing the new one
			#Show current settings for TCP. This will be enabled once the client code and config file code has been written
			print("TCP settings menu:")
			print("1. Change host and/or port")
			print("2. Test current connection")
			print("3. Return to main menu")
			if wrong_ch:
				choice = input("Enter a correct number please: ")
				wrong_ch = False
			else:
				choice = input("Enter your menu choice: ")
			
			#Control to be added
			if choice == "1":
				self.cls() #Clear the previous menu before showing the new one
				print("\nEnter the server host name e.g. \"localhost\" or 127.0.0.1:")
				host = input() #Get the host name from the user
				print("The entered host is: " + host)
				continue #Stay in the TCP menu
			elif choice == "2":
				while(True):
					self.cls() #Clear the previous menu before showing the new one
					if wrong_ch:
						print("Please give an integer as the server port: ")
					else:
						print("\nEnter the server port as an integer e.g. 10001: ")
					try:
						port = int(input("Enter port: "), 10)
						break
					except:
						wrong_ch = True
						continue
				continue #Stay in the TCP menu
			#Third choice to be added
			elif choice == "3":
				break
			else:
				wrong_ch = True

	def transitMenu(self):
		self.cls() #Clear the previous menu before showing the new one
		print("Transit menu:")
		print("1. Provide transit point coordinates (Dec/RA)")
		print("2. Choose time for the currently chosen object")
		print("3. Return to main menu")
		choice = input("Enter your menu choice: ")
		
		#Control to be added
	
	def objectMenu(self):
		self.cls() #Clear the previous menu before showing the new one
		print("Object choice menu:")
		print("1. Sun")
		print("2. Moon")
		print("3. Jupiter")
		print("4. Return to main menu")
		choice = input("Enter your menu choice: ")
		
		#Control to be added
	
	def setAngle(self, angName):
		print("\nEnter the " + angName + " in decimal degrees.")
		print("For a south Latitude or a weste Longitude, enter a minus sign in the decimal value.")
		return input(angName + ": ") #Return the angle entered by the user
	
	def cls(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		self.intro()


#Initial test code

uInterface().mainMenu()