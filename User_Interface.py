#Import the required libraries
import os
from showMenu import showMenu
from time import sleep

class uInterface(object):
    def __init__(self, cfgData, clientSocket):
        print("Getting TCP connection status...")
        self.clientSocket = clientSocket
        self.cfgData = cfgData
        self.conStatus = self.clientSocket.sendRequest("Test")
        self.mainMenu()
    
    def mainMenu(self):
        while(True):
            print("Getting TCP connection status...")
            self.conStatus = self.clientSocket.sendRequest("Test") #Get the connection status
            #sleep(1) #Use that in order for the user to be able and see the message
            self.cls() #Clear the previous menu before showing the new one
            
            #Create the necessary string according to the autoconnection setting
            if self.cfgData.getTCPAutoConnStatus() == "yes":
                autoCon_st = "Enabled"
            else:
                autoCon_st = "Disabled"
            
            #Show the current configuration and status in the main menu
            print("***********************************************")
            print("-->Current status:")
            print("   [*]Location:")
            print("         >Latitude:    %s" %self.cfgData.getLatLon()[0] + u"\u00b0")
            print("         >Longitude:   %s" %self.cfgData.getLatLon()[1] + u"\u00b0")
            print("         >Altitude:    %s" %self.cfgData.getAltitude() + "m")
            print("   [*]TCP status:")
            if self.conStatus == "OK":
                print("         >Connected to %s:%s" %(self.cfgData.getHost(), self.cfgData.getPort()))
                print("         >Autoconnect: %s" %autoCon_st)
            else:
                print("         >Disconnected")
                print("         >Autoconnect: %s" %autoCon_st)
            print("***********************************************")
            
            showMenu().main() #Show the main menu items
            choice = input("Enter your menu choice: ")
            
            if choice == "2":
                self.objectMenu()
            elif choice == "3":
                self.transitMenu()
            elif choice == "5":
                self.TCPMenu()
            elif choice == "6":
                self.locationMenu()
            elif choice == "7":
                #Additional code may be added if some other processes are active, to terminate them
                print("\nDisconnecting from server...")
                if self.clientSocket.sendRequest("Terminate") == "Bye":
                    
                    print("Successfully disconnected from server.")
                else:
                    print("There was a problem contacting the server, although the connection was closed.")
                self.clientSocket.disconnect()
                print("\nGoodbye! See you again later!")
                sleep(2)
                break #Terminate the program

    def locationMenu(self):
        wrong_ch = False #Indicate if there is a wrong choice input from the user
        
        s_latlon = self.cfgData.getLatLon() #First element is latitude and second element is logitude
        s_alt = self.cfgData.getAltitude() #Get the altitude from the settings file
        
        while(True):
            loc_updt = self.cfgData.getUpdateStatus("location") #See if the location has been updated
            self.cls() #Clear the previous menu before showing the new one
            
            #Show current settings for the location
            print("****************************")
            if loc_updt == "yes":
                print("->Currently set location (updated):")
                self.cfgData.setUpdateStatus("location", "no")
            else:
                print("->Currently set location:")
            print("   [*]Latitude:  %s" %s_latlon[0] + u"\u00b0")
            print("   [*]Longitude: %s" %s_latlon[1] + u"\u00b0")
            print("   [*]Altitude:  %s" %s_alt + "m")
            print("****************************")
            
            showMenu().location() #Show the menu items for the location
            
            #Handle what happens with a wrong input
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
                        self.cfgData.setUpdateStatus("location", "no")
                    else:
                        #Set the latitude, longitude and altitude in the settings file
                        self.cfgData.setLatLon(s_latlon)
                        self.cfgData.setAltitude(s_alt)
                        s_latlon = [lat, lon]
                        s_alt = alt
                    continue
            elif choice == "2":
                break #Get out from the loop and return to main menu
            else:
                wrong_ch = True

    def TCPMenu(self):
        wrong_ch = False #Wrong choice indicator
        serv_change = False #Server change indicator
        
        #Read TCP settings from the XML configuration file
        s_host = self.cfgData.getHost()
        s_port = int(self.cfgData.getPort())
        s_autocon = self.cfgData.getTCPAutoConnStatus()
        
        while(True):
            #Get the client's connection status with the server
            print("Getting TCP connection status...")
            self.conStatus = self.clientSocket.sendRequest("Test") #Get the connection status
            tcp_updt = self.cfgData.getUpdateStatus("TCP") #See if the TCP has been updated
            self.cls() #Clear the previous menu before showing the new one
            
            #Show current settings for TCP
            print("**********************************")
            if tcp_updt == "yes":
                print("->Current TCP settings (updated):")
                self.cfgData.setUpdateStatus("TCP", "no")
            else:
                print("->Current TCP settings:")
            print("   [*]Host: %s" %s_host)
            print("   [*]Port: %s" %s_port)
            if s_autocon == "yes":
                print("   [*]Autoconnect: Enabled")
            else:
                print("   [*]Autoconnect: Disabled")
            
            #Also show the client's connection status to the server
            print("**********************************")
            if self.conStatus == "OK":
                print("->Client Status: Connected")
            else:
                print("->Client Status: Disconnected")
            print("**********************************")
            
            showMenu().TCP() #Show the TCP menu choices
            
            #Show additional menu options, depending on the connection status
            if self.conStatus != "OK":
                print("   4. Connect to server")
                print("   5. Return to main menu")
            else:
                print("   4. Return to main menu")
            
            #Wrong choice input handling
            if wrong_ch:
                choice = input("Enter a correct number please: ")
                wrong_ch = False
            else:
                choice = input("Enter your menu choice: ")
            
            if choice == "1":
                self.cls() #Clear the previous menu before showing the new one
                
                #Host input section
                print("\nEnter the server host name e.g. \"localhost\" or 127.0.0.1.\nThe current host is \'%s\'" %s_host)
                host = input("Host: ") #Get the host name from the user
                print("The entered host is: " + host)
                
                #Port input section
                while(True):
                    if wrong_ch:
                        print("Please give an integer as the server port: ")
                        wrong_ch = False
                    else:
                        print("\nNow enter the server port as an integer e.g. 10001.\nThe current port is %s" %s_port)
                    try:
                        port = int(input("Port: "), 10) #Convert string from input to decimal integer
                        break
                    except:
                        wrong_ch = True
                        continue
                
                #Provide the user with a summary of what was entered
                print("\nThe entered parameters for the server are:")
                print("Host: %s\nPort: %s\n" %(host, port))
                
                #Ask if the parameters are accepted by the user
                print("Do you accept the parameters? If yes, the current connection, if any, will be aborted.")
                print("If the parameters entered are the same as the current ones, no connection will be aborted.")
                acc = input("Do you agree with the above? If yes type 'y', otherwise type anything: ")
                
                '''
                    If statement to check if the port and the host are the same as the saved ones. If they are not both the same change serv_change to True.
                    If both are the same, just return to the TCP menu.
                    First ask the user if the values entered are accepted and then move on.
                    If there are new values entered, and the user accepts them, inform the user that the current connection, if any, will be aborted,
                    And the values are going to be chaged.
                    Also ask the user if he wants a connection to be made with the new values.
                '''
                if acc == "y":
                    if (s_host == host) and (s_port == port):
                        self.cfgData.setUpdateStatus("TCP", "no")
                        serv_change = False
                    else:
                        print("\nDisconnecting from server...")
                        if self.clientSocket.sendRequest("Terminate") == "Bye":
                            self.clientSocket.disconnect() #Disconnect from the current connection
                            print("Disconnected from server.")
                            serv_change = True
                        else:
                            print("Couldn\'t terminate properly, but the new settings will be saved.")
                        self.cfgData.setHost(host) #Save the host in the settings file
                        self.cfgData.setPort(port) #Save the port in the settings file
                        s_host = host #Update the saved host
                        s_port = port #Update the saved port
                    sleep(1) #Pause for one second so the message is visible
                
                #If there was success in disconnecting after setting update, do the following
                if serv_change:
                    print("\nDo you want to establish a connection with the new server?")
                    acc = input("If yes type 'y', otherwise type anything: ")
                    if acc == "y":
                        self.clientSocket.connect(s_host, s_port) #Connect to the new server
                        if self.clientSocket.sendRequest("Test") == "OK":
                            print("Succesfully connected with the server.")
                        else:
                            print("There was a communication problem with the server.")
                    sleep(1) #Pause for one second so the message is visible
                continue #Stay in the TCP menu
                
            elif choice == "2":
                print("\nTrying to connect to the server.")
                print("The details of the server are %s:%s" %(s_host, s_port))
                self.conStatus = self.clientSocket.sendRequest("Test")
                
                #Output messages according to the prevoius result of connection status
                if self.conStatus == "OK":
                    print("\nSuccesfully contacted the server.")
                else:
                    print("\nUnfortunately, communication with the server was imposible.")
                sleep(2) #Keep the message for two seconds
                
            elif choice == "3":
                if s_autocon == "yes":
                    self.cfgData.TCPAutoConnDisable() #Disable the autoconnection and save the setting
                    s_autocon = self.cfgData.getTCPAutoConnStatus()
                else:
                    self.cfgData.TCPAutoConnEnable() #Enable the autoconnection and save the setting
                    s_autocon = self.cfgData.getTCPAutoConnStatus()
                    
            elif choice == "4":
                if self.conStatus == "OK": #If the program is already connected to a server, there nothing to do here
                    break
                else: #If the program is not connected to a server, do the following
                    print("\nConnecting to server %s:%s\n" %(s_host, s_port))
                    if self.clientSocket.connect(s_host, s_port):
                        contct = self.clientSocket.sendRequest("Test") #Try to make a contact with the server
                        if contct == "OK": #If contact was made, print the following
                            print("Successfully connected to the server %s:%s" %(s_host, s_port))
                            print("And also made contact with the server.")
                            sleep(2)
                    else:
                        print("Failed to connect to the server %s:%s" %(s_host, s_port))
                        sleep(2)
            
            #Choice No.5 will be available if an only if the client is not connected to the server
            elif (choice == "5") and (self.conStatus != "OK"):
                break #Return to main menu
            else:
                wrong_ch = True #Reiterrate. Show the appropriate message to the user

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
