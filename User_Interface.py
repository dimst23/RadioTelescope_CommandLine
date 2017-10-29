import os

class uInterface(object):
	def mainMenu(self):
		print("Main Menu:")
		print("1. Read Position")
		print("2. Choose object")
		print("3. Transit")
		print("4. Aim and guide")
		print("5. TCP settings")
		print("6. Location settings")
		print("Enter your menu choice: ")
		
		inp = input()
		
		#Initialy for testing
		if inp == "6":
			self.cls()

	def locationMenu(self):
		#Show current settings on the top. That will be done latter after deciding for the final menu outline
		print("Location Menu:")
		print("1. Keep current location")
		print("2. Set new location")
		print("3. Return to main menu")
		#Control to be added

	def TCPMenu(self):
		print("TCP settings menu:")
		print("1. Change address")
		print("2. Chage host")
		print("3. Test current connection")
		print("4. Return to main menu")
		#Control to be added

	def transitMenu(self):
		print("Transit menu:")
		print("1. Provide transit point coordinates (Dec/RA)")
		print("2. Choose time for the currently chosen object")
		print("3. Return to main menu")
	
	def cls(self):
		os.system('cls' if os.name == 'nt' else 'clear')


uInterface().mainMenu()