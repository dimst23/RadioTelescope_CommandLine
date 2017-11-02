class showMenu(object):
	def intro(self):
		print("***********************************************")
		print("**  A.U.Th Radio Telescope Control Software  **")
		print("**                                           **")
		print("**  by Dimitrios Stoupis - dstoupis@auth.gr  **")
		print("***********************************************")
		
	def main(self):
		print("Main Menu:")
		print("   1. Read Position")
		print("   2. Choose object")
		print("   3. Transit")
		print("   4. Aim and guide")
		print("   5. TCP settings")
		print("   6. Location settings")
		print("   7. Exit program")
	
	def location(self):
		print("Location Menu:")
		print("   1. Set new location")
		print("   2. Return to main menu")
	
	def TCP(self):
		print("TCP settings menu:")
		print("   1. Change host and/or port")
		print("   2. Test current connection")
		print("   3. Enable/Disable startup autoconnect")
	
	def transit(self):
		print("Transit menu:")
		print("   1. Provide transit point coordinates (Dec/RA)")
		print("   2. Choose time for the currently chosen object")
		print("   3. Return to main menu")
	
	def object(self):
		print("Object choice menu:")
		print("   1. Sun")
		print("   2. Moon")
		print("   3. Jupiter")
		print("   4. Return to main menu")