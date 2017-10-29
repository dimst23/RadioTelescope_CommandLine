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
		self.cls() #Clear the previous menu before showing the new one
		print("Main Menu:")
		print("1. Read Position")
		print("2. Choose object")
		print("3. Transit")
		print("4. Aim and guide")
		print("5. TCP settings")
		print("6. Location settings")
		print("Enter your menu choice: ")
		
		choice = input()
		
		if choice == "2":
			self.cls() #Clear the previous menu before showing the new one
			self.objectMenu()
		elif choice == "3":
			self.cls() #Clear the previous menu before showing the new one
			self.transitMenu()
		elif choice == "5":
			self.cls() #Clear the previous menu before showing the new one
			self.TCPMenu()
		elif choice == "6":
			self.cls() #Clear the previous menu before showing the new one
			self.locationMenu()

	def locationMenu(self):
		#Show current settings on the top. That will be done latter after deciding for the final menu outline
		print("Location Menu:")
		print("1. Keep current location")
		print("2. Set new location")
		print("3. Return to main menu")
		print("Enter your menu choice: ")
		
		choice = input()
		#Control to be added

	def TCPMenu(self):
		print("TCP settings menu:")
		print("1. Change host")
		print("2. Chage port")
		print("3. Test current connection")
		print("4. Return to main menu")
		print("Enter your menu choice: ")
		
		choice = input()
		#Control to be added

	def transitMenu(self):
		print("Transit menu:")
		print("1. Provide transit point coordinates (Dec/RA)")
		print("2. Choose time for the currently chosen object")
		print("3. Return to main menu")
		print("Enter your menu choice: ")
		
		choice = input()
		#Control to be added
	
	def objectMenu(self):
		print("Object choice menu:")
		print("1. Sun")
		print("2. Moon")
		print("3. Jupiter")
		print("4. Return to main menu")
		print("Enter your menu choice: ")
		
		choice = input()
		#Control to be added
	
	def cls(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		self.intro()


#Initial test code
uInterface().cls()

uInterface().mainMenu()