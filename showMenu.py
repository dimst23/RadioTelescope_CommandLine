class showMenu(object):
    def intro(self):
        print("***********************************************")
        print("**  A.U.Th Radio Telescope Control Software  **")
        print("**                                           **")
        print("**  by Dimitrios Stoupis - dstoupis@auth.gr  **")
        print("***********************************************")
        
    def main_con(self):
        print("Main Menu:")
        print("   1. Read Position")
        print("   2. Choose object")
        print("   3. Control menu")
        #print("   3. Transit")
        #print("   4. Aim and guide")
        print("   4. TCP settings")
        print("   5. Location settings")
        print("   6. Exit program")
        
    def main_nocon(self):
        print("Main Menu (Some choices hidden):")
        print("   1. Choose object")
        print("   2. TCP settings")
        print("   3. Location settings")
        print("   4. Exit program")
    
    def location(self):
        print("Location Menu:")
        print("   1. Set new location")
        print("   2. Return to main menu")
    
    def TCP(self):
        print("TCP settings menu:")
        print("   1. Change host and/or port")
        print("   2. Test current connection")
        print("   3. Enable/Disable startup auto-connect")
    
    def transit(self):
        print("Transit menu:")
        print("   1. Choose time for the currently chosen object")
        print("   2. Return to main menu")
    
    def object(self):
        print("Object choice menu:")
        print("   1. Sun")
        print("   2. Moon")
        print("   3. Jupiter")
        print("   4. Enter an object manually")
        print("   5. Return to main menu")