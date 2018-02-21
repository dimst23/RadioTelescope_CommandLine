#Import the required libraries
from showMenu import showMenu
from time import sleep
import logData
import ephem
import time
import os

_rad_to_deg = 57.2957795131 #Conversion constant for converting rad to degrees

#General Notes
'''
   Include returning to home position when closing the program 
'''

class uInterface(object):
    def __init__(self, cfgData, clientSocket):
        lalon = cfgData.getLatLon() #Get the current latitude longitude for the observer
        self.clientSocket = clientSocket #Set a TCP client socket handling variable
        self.cfgData = cfgData #Set the XML file's handling variable
        self.observer = ephem.Observer() #Set an observer variable
        self.observer.lon, self.observer.lat = lalon[1], lalon[0] #Set the current observer position according to the currently saved settings
        self.logdata = logData.logData(__name__) #Initiate a logger for the current file
        self.mainMenu() #Start the main menu
    
    def mainMenu(self):
        while(True):
            print("Getting TCP connection status...") #Tell the user that the program is waiting for the TCP connection (20 second timeout)
            conStatus = self.clientSocket.sendRequest("Test") #Get the connection status
            choice = "" #User input variable which is required to be global for this function
            #sleep(1) #Use that in order for the user to be able and see the message
            self.cls() #Clear the previous menu before showing the new one
            
            #Get the currently saved object
            cur_obj = self.cfgData.getObject()
            hostport = [self.cfgData.getHost(), self.cfgData.getPort()]
            
            #Create the necessary string according to the auto-connection setting
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
            if conStatus == "OK":
                print("         >Connected to %s:%s" %(hostport[0], hostport[1]))
                print("         >Autoconnect: %s" %autoCon_st)
            else:
                print("         >Disconnected")
                print("         >Autoconnect: %s" %autoCon_st)
                self.logdata.log("WARNING", "Could not connect to %s:%s and the auto-connection is %s." %(hostport[0], hostport[1], autoCon_st), "mainMenu")
            print("   [*]Selected object:")
            if cur_obj[1] == -1:
                print("         >Name: %s" %cur_obj[0])
            else:
                print("         >Name: %s" %cur_obj[0])
                print("         >RA :  %s" %cur_obj[1] + u"\u00b0")
                print("         >DEC:  %s" %cur_obj[2] + u"\u00b0")
            print("***********************************************")
            
            #Show the correct menu according to the connection status with the server
            if conStatus == "OK":
                showMenu().main_con() #Show the all main menu items
                try:
                    choice = input("Enter your menu choice: ")
                except:
                    self.logdata.log("WARNING", "User requested termination with a keyboard interrupt.", "mainMenu")
                    pass
                
                if choice == "1":
                    self.positionMenu()
                elif choice == "2":
                    self.objectMenu()
                elif choice == "3":
                    self.controlMenu()
                elif choice == "4":
                    self.TCPMenu()
                elif choice == "5":
                    self.locationMenu()
                elif choice == "6":
                    #Additional code may be added if some other processes are active, to terminate them
                    print("\nDisconnecting from server...")
                    if self.clientSocket.sendRequest("Terminate") == "Bye":
                        print("Successfully disconnected from server.")
                        self.logdata.log("INFO", "Successfully disconnected from server.", "mainMenu")
                    else:
                        print("There was a problem contacting the server, although the connection was closed.")
                        self.logdata.log("WARNING", "There was a problem contacting the server, although the connection was closed.", "mainMenu")
                    self.clientSocket.disconnect() #Disconnect from the server before closing the program
                    self.logdata.logClose() #Terminate all logging processes before exiting the program
                    print("\nGoodbye! See you again later!")
                    sleep(2) #Used to keep the above message alive for the user to see it
                    break #Terminate the program
            else:
                showMenu().main_nocon() #Show restricted menu items because there is no connection with the TCP server
                try:
                    choice = input("Enter your menu choice: ")
                except EOFError:
                    self.logdata.log("WARNING", "User requested termination with a keyboard interrupt.", "mainMenu")
                    pass
                
                if choice == "1":
                    self.objectMenu()
                elif choice == "2":
                    self.TCPMenu()
                elif choice == "3":
                    self.locationMenu()
                elif choice == "4":
                    #Additional code may be added if some other processes are active, to terminate them
                    self.logdata.logClose() #Terminate all logging processes before exiting the program
                    print("\nGoodbye! See you again later!")
                    sleep(2) #Used to keep the above message alive for the user to see it
                    break #Terminate the program

    def locationMenu(self):
        choice = "" #User input variable which is required to be global for this function
        
        s_latlon = self.cfgData.getLatLon() #First element is latitude and second element is longitude
        s_alt = self.cfgData.getAltitude() #Get the altitude from the settings file
        
        while(True):
            loc_updt = self.cfgData.getUpdateStatus("location") #See if the location has been updated
            self.cls() #Clear the previous menu before showing the new one
            
            #Show current settings for the location
            print("****************************")
            if loc_updt == "yes":
                print("->Currently set location (updated):")
                self.locupdate = True
                self.cfgData.setUpdateStatus("location", "no")
            else:
                print("->Currently set location:")
            print("   [*]Latitude:  %s" %s_latlon[0] + u"\u00b0")
            print("   [*]Longitude: %s" %s_latlon[1] + u"\u00b0")
            print("   [*]Altitude:  %s" %s_alt + "m")
            print("****************************")
            
            showMenu().location() #Show the menu items for the location
            
            #Get the input from user
            try:
                choice = input("Enter your menu choice: ")
            except EOFError:
                self.logdata.log("WARNING", "User requested termination with a keyboard interrupt.", "locationMenu")
                pass
            
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
                        self.observer.lat, self.observer.lon = s_latlon[0], s_latlon[1] #Also update the current observer
                    continue
            elif choice == "2":
                break #Get out from the loop and return to main menu

    def TCPMenu(self):
        wrong_ch = False #Wrong choice indicator
        serv_change = False #Server change indicator
        
        #Set the variables for the host and port input
        port = 0 #Default value for debugging
        host = "" #Default value for debugging
        
        #Read TCP settings from the XML configuration file
        s_host = self.cfgData.getHost()
        s_port = int(self.cfgData.getPort())
        s_autocon = self.cfgData.getTCPAutoConnStatus()
        
        while(True):
            #Get the client's connection status with the server
            print("Getting TCP connection status...")
            conStatus = self.clientSocket.sendRequest("Test") #Get the connection status
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
            if conStatus == "OK":
                print("->Client Status: Connected")
            else:
                print("->Client Status: Disconnected")
            print("**********************************")
            
            showMenu().TCP() #Show the TCP menu choices
            
            #Show additional menu options, depending on the connection status
            if conStatus != "OK":
                print("   4. Connect to server")
                print("   5. Return to main menu")
            else:
                print("   4. Return to main menu")
            
            #Wrong choice input handling
            try:
                if wrong_ch:
                    choice = input("Enter a correct number please: ")
                else:
                    choice = input("Enter your menu choice: ")
                wrong_ch == False #Reset the indicator
            except EOFError:
                self.logdata.log("WARNING", "User requested termination with a keyboard interrupt.", "TCPMenu")
                pass
            
            if choice == "1":
                self.cls() #Clear the previous menu before showing the new one
                
                #Host input section
                print("\nEnter the server host name e.g. \"localhost\" or 127.0.0.1.\nThe current host is \'%s\'" %s_host)
                print("If you want to keep host the same, just press enter and do not enter anything.")
                try:
                    host = input("Host: ") #Get the host name from the user
                    if host == "":
                        host = s_host
                    else:
                        print("The entered host is: " + host)
                except EOFError:
                    pass
                
                #Port input section
                while(True):
                    if wrong_ch:
                        print("Please give an integer as the server port: ")
                        wrong_ch = False
                    else:
                        print("\nNow enter the server port as an integer e.g. 10001.\nThe current port is %s" %s_port)
                        print("If you do not want to change the port and leave it as it is, just press enter.")
                    try:
                        port = input("Port: ")
                        if port == "":
                            port = s_port
                        else:
                            port = int(port, 10) #Convert string from input to decimal integer
                        break
                    except ValueError:
                        wrong_ch = True
                        continue
                    except:
                        pass
                
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
                    And the values are going to be changed.
                    Also ask the user if he wants a connection to be made with the new values.
                '''
                if acc == "y":
                    if (s_host == host) and (s_port == port):
                        self.cfgData.setUpdateStatus("TCP", "no") #Indicate that no update has been made
                        serv_change = False #Make sure the change indicator is set to False
                    elif conStatus == "OK":
                        print("\nDisconnecting from server...")
                        if self.clientSocket.sendRequest("Terminate") == "Bye":
                            self.clientSocket.disconnect() #Disconnect from the current connection
                            print("Disconnected from server.") #Inform the user for successful disconnection
                            self.logdata.log("INFO", "TCP disconnected from server.", "TCPMenu") #Log the server disconnection
                            serv_change = True
                        else:
                            print("Could not terminate properly, but the new settings will be saved.")
                            self.logdata.log("WARNING", "Could not terminate properly, but the new settings will be saved.", "TCPMenu")
                    else:
                        serv_change = True #Indicate server change
                        print("Server details changed to %s:%s" %(host, port))
                        self.logdata.log("WARNING", "Server connection details changed to %s:%s" %(host, port), "TCPMenu")
                    self.cfgData.setHost(host) #Save the host in the settings file
                    self.cfgData.setPort(port) #Save the port in the settings file
                    s_host = host #Update the saved host
                    s_port = port #Update the saved port
                    sleep(1) #Pause for one second so the message is visible
                
                #If there was success in disconnecting after setting update, do the following
                if serv_change:
                    print("\nDo you want to establish a connection with the new server settings?")
                    acc = input("If yes type 'y', otherwise type anything: ")
                    if acc == "y":
                        self.clientSocket.connect(s_host, s_port) #Connect to the new server
                        if self.clientSocket.sendRequest("Test") == "OK":
                            print("Successfully connected with the server.")
                        else:
                            print("There was a communication problem with the server.")
                            self.logdata.log("WARNING", "There was a communication problem with the server.", "TCPMenu")
                    sleep(1) #Pause for one second so the message is visible
                
            elif choice == "2":
                print("\nTrying to connect to the server.")
                print("The details of the server are %s:%s" %(s_host, s_port))
                conStatus = self.clientSocket.sendRequest("Test") #Send the test command to the server and await for its response
                
                #Output messages according to the previous result of connection status
                if conStatus == "OK":
                    print("\nSuccesfully contacted the server.")
                else:
                    print("\nUnfortunately, communication with the server was impossible.")
                    self.logdata.log("WARNING", "Unfortunately, communication with the server was impossible.", "TCPMenu")
                sleep(2) #Keep the message for two seconds
            
            #There is no menu for the auto-connection change, it just toggles
            elif choice == "3":
                if s_autocon == "yes":
                    self.cfgData.TCPAutoConnDisable() #Disable the auto-connection and save the setting
                    s_autocon = self.cfgData.getTCPAutoConnStatus()
                else:
                    self.cfgData.TCPAutoConnEnable() #Enable the auto-connection and save the setting
                    s_autocon = self.cfgData.getTCPAutoConnStatus()
                    
            elif choice == "4":
                if conStatus == "OK": #If the program is already connected to a server, there nothing to do here
                    break
                else: #If the program is not connected to a server, do the following
                    self.clientSocket.disconnect() #Disconnect is used to create a new socket to enable reconnection of a lost connection
                    print("\nConnecting to server %s:%s\n" %(s_host, s_port)) #Indicate to the user that a connection attempt will be done
                    
                    if self.clientSocket.connect(s_host, s_port): #On successful connection execute the following code
                        contct = self.clientSocket.sendRequest("Test") #Try to make a contact with the server
                        if contct == "OK": #If contact was made, print the following
                            print("Successfully connected to the server %s:%s" %(s_host, s_port))
                            print("And also made contact with the server.")
                            self.logdata.log("INFO", "Client successfully connected to %s:%s." %(s_host, s_port), "TCPMenu")
                    else:
                        print("Failed to connect to the server %s:%s" %(s_host, s_port))
                        self.logdata.log("WARNING", "Failed to connect to the server %s:%s" %(s_host, s_port), "TCPMenu")
                    sleep(2)
            
            #Choice No.5 will be available if an only if the client is not connected to the server
            elif (choice == "5") and (conStatus != "OK"):
                break #Return to main menu
            else:
                wrong_ch = True #Reiterate. Show the appropriate message to the user

    def controlMenu(self):
        choice = "" #User input variable
        cur_pos = "" #Position holding variable
        wrong_ch = False #Indicator of correct menu number
        serv_con = False #Server connection status indicator
        
        while(True):
            #Show the currently chosen object
            chosen_body = self.cfgData.getObject() #Get the currently chosen object
            
            if self.clientSocket.sendRequest("Test") == "OK":
                #Add code to check if we are connected to the server first
                serv_con = True #Indicate active server
                cur_pos = self.clientSocket.sendRequest("Report Position")
                if cur_pos == "No answer":
                    cur_pos = "Not available"
                    self.logdata.log("WARNING", "The current telescope position is not available.", "controlMenu")
                else:
                    cur_pos = cur_pos.split("_")
                    self.logdata.log("INFO", "The current telescope position is\nRA: %s\nDEC: %s" %(cur_pos[1], cur_pos[2]), "controlMenu")
            else:
                self.logdata.log("WARNING", "The connection with the server has been lost.", "controlMenu")
                serv_con = False #Indicate inactive server
                cur_pos = "Not available"
            
            self.cls()
            print("***********************************************")
            print("   [*]Selected object:")
            if chosen_body[1] == -1:
                print("         >Name: %s" %chosen_body[0])
            else:
                print("         >Name: %s" %chosen_body[0])
                print("         >RA :  %s" %chosen_body[1] + u"\u00b0")
                print("         >DEC:  %s" %chosen_body[2] + u"\u00b0")
            print("   [*]Telescope status:")
            #Add code for tracking status checking
            print("         >Tracking: ")
            
            if cur_pos == "Not available":
                print("         >Position: %s" %cur_pos)
            else:
                print("         >Position: ")
                print("             *RA : %s" %cur_pos[1] + u"\u00b0")
                print("             *DEC: %s" %cur_pos[2] + u"\u00b0")
            print("***********************************************")
            
            #Show if the telescope is now tracking or not (check that by asking the appropriate command through the TCP)
            #Show the current position of the telescope if not tracking (use the appropriate command to get the dish's position)
            
            if serv_con:
                showMenu().control() #Show the menu options
                try:
                    if wrong_ch:
                        choice = input("Please provide a correct number: ")
                    else:
                        choice = input("Enter your menu choice: ")
                    wrong_ch == False #Reset the indicator
                except EOFError:
                    self.logdata.log("WARNING", "User requested termination with a keyboard interrupt.", "controlMenu")
                    pass
                
                if choice == "1":
                    self.transitMenu()
                elif choice == "2":
                    self.trackingMenu()
                elif choice == "3":
                    #self.scanningMenu()
                    break #Added until the above function is complete
                elif choice == "4":
                    #self.skyscanMenu()
                    break #Added until the above function is complete
                elif choice == "5":
                    break #Return to main menu
                else:
                    wrong_ch = True #Indicate a wrong choice input
            else:
                print("For some reason server is not connected so no option can be executed.")
                input("Press enter or type anything to return to main menu: ")
                break
    
    def transitMenu(self):
        #Declare some variable that are later required and initialize them
        obj_ra = "-1"
        obj_dec = "-1"
        man_ra = "-1"
        man_dec = "-1"
        choice = "" #User input variable
        
        while(True):
            chosen_body = self.cfgData.getObject() #Get the currently chosen object
            self.cls() #Clear the previous menu before showing the new one
            print("***********************************************")
            
            print("   [*]Selected object:")
            if chosen_body[1] == -1:
                print("         >Name: %s" %chosen_body[0])
            else:
                print("         >Name: %s" %chosen_body[0])
                print("         >RA :  %s" %chosen_body[1])
                print("         >DEC:  %s" %chosen_body[2])
            print("***********************************************")
            
            showMenu().transit() #Show the user interface for this menu
            try:
                choice = input("Enter your menu choice: ")
            except EOFError:
                self.logdata.log("WARNING", "User requested termination with a keyboard interrupt.", "transitMenu")
                pass
            
            if choice == "1":
                self.cls()
                print("Give a transit time, in 24hr format, which is after the time that enter will be pressed (at least 1 minute).")
                print("For better results, provide a time at least 10 minutes from the current time.")
                
                '''
                    Get the time from the user and then check if it is the same as the current time.
                    If it is then inform the user and ask for another entry.
                    If the time is good, then proceed by taking the current date and combining it with the given time in a string.
                    The above string will be used as an input to calculate the ephemeris data of the non stationary bodies.
                    time.gmtime(), tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec
                '''
                t_obj = time.gmtime() #Get the return from the gmtime function to use it in the date creation
                tim = input("Give the transit time in UTC by separating hours, minutes, seconds with ':' (e.g. '20:12:34'): ")
                while(True): #Make sure correct time input
                    t_obj = time.gmtime() #Get the current time
                    temp = tim.split(":") #Take the time components
                    try:
                        if int(temp[0]) < 24 or int(temp[1]) <= 59 or int(temp[2]) <= 59: #Check if the time is correct
                            if int(temp[0]) > int(t_obj.tm_hour) or ((int(t_obj.tm_hour) == int(temp[0])) 
                                and (int(t_obj.tm_min) - (int(temp[1])) is not 0) and (int(temp[1]) > int(t_obj.tm_min))):
                                break
                            else:
                                tim = input("Please enter a correct time. Current UTC time is %s:%s:: " %(t_obj.tm_hour, t_obj.tm_min))
                    except ValueError:
                        tim = input("Please enter a correct time. Current time is %s:%s UTC: " %(t_obj.tm_hour, t_obj.tm_min))
                
                #If everything succeeds from the control, then move on with the following
                date = "%s/%s/%s" %(t_obj.tm_year, t_obj.tm_mon, t_obj.tm_mday) #Save the date in a string in the appropriate format
                eph_t_date = "%s %s" %(date, tim) #Make the correct date time string to be used to calculated ephemeris
                
                if chosen_body[0] == "Sun":
                    sun = ephem.Sun()
                    sun.compute(eph_t_date, epoch = date) #Calculate ephemeris at the current date
                    obj_ra = float(sun.a_ra)*_rad_to_deg
                    obj_dec = float(sun.a_dec)*_rad_to_deg
                elif chosen_body[0] == "Moon":
                    moon = ephem.Moon()
                    moon.compute(eph_t_date, epoch = date) #Calculate ephemeris at the current date
                    obj_ra = float(moon.a_ra)*_rad_to_deg
                    obj_dec = float(moon.a_dec)*_rad_to_deg
                elif chosen_body[0] == "Jupiter":
                    jup = ephem.Jupiter()
                    jup.compute(eph_t_date, epoch = date) #Calculate ephemeris at the current date
                    obj_ra = float(jup.a_ra)*_rad_to_deg
                    obj_dec = float(jup.a_dec)*_rad_to_deg
                else:
                #Add control to what to do with stationary bodies
                    obj_ra = float(chosen_body[1])
                    obj_dec = float(chosen_body[2])
                
                #The hour angle of the object is LST (Local Sidereal Time) - a (Right Ascension)
                self.observer.date = eph_t_date #Set the observer's date
                hour_ang = float(self.observer.sidereal_time())*_rad_to_deg - obj_ra #ephem sidereal returns in rad
                
                #Add control for the negative value of the hour angle
                #When the hour angle is negative then add 360 to make it positive if you wish, or indicate leftward direction, provided that the 0 position is south
                self.logdata.log("INFO", "Transit command sent\nObject: %s\nSidereal Time: %.5f\nRA: %.5f\nDEC: %.5f\nHour angle: %.5f" 
                    %(chosen_body[0], float(self.observer.sidereal_time())*_rad_to_deg, obj_ra, obj_dec, hour_ang), "transitMenu")
                #sleep(5) #Used for testing
                
                #Send the request for the transit along with the required information to the Raspberry Pi
                rsp = self.clientSocket.sendRequest("TRNST_RA_%.5f_DEC_%.5f" %(hour_ang, obj_dec)) #Send the transit request and get the response
                if rsp == "No answer":
                    rsp = self.clientSocket.longWait_rcv(60) #Wait to receive the response for 60 seconds, because the dish can take time to reach position
                
                if rsp == "POSITION_SET":
                    print("The telescope is at its position for transit.")
                    self.logdata.log("INFO", "The telescope is at its position for transit.", "transitMenu")
                else:
                    print("There was a problem with setting the telescopes position. %s" %rsp)
                    self.logdata.log("WARNING", "There was a problem with setting the telescopes position. Server sent: %s" %rsp, "transitMenu")
                    break #Return to control menu
                
            elif choice == "2":
                break      
    
    def trackingMenu(self):
        #Declare some variable that are later required and initialize them
        obj_ra = "-1"
        obj_dec = "-1"
        cur_stp_ra = 0
        cur_stp_dec = 0
        
        #Number of steps per degree for the motors
        stpp_deg_ra = 0
        stpp_deg_dec = 0
        
        start_time = 0 #Variable to hold the time delay where the tracking starts after setting the dish position
        
        chosen_body = self.cfgData.getObject() #Get the currently chosen object
        self.cls()
        print("***********************************************")
        print("   [*]Selected object:")
        if chosen_body[1] == -1:
            print("         >Name: %s" %chosen_body[0])
        else:
            print("         >Name: %s" %chosen_body[0])
            print("         >RA :  %s" %chosen_body[1] + u"\u00b0")
            print("         >DEC:  %s" %chosen_body[2] + u"\u00b0")
        print("***********************************************")
        
        print("Tracking Menu")
        track_time = input("Enter for how long you want the object to be tracked in seconds: ")
        
        t_obj = time.gmtime() #Get the return from the gmtime function to use it in the date creation
        date = "%s/%s/" %(t_obj.tm_year, t_obj.tm_mon) #Save the date in a string in the appropriate format
        cur_time_d = float(t_obj.tm_mday) + float(t_obj.tm_hour)/24.0 + float(t_obj.tm_min/1440.0) + float(t_obj.tm_sec/86400.0)
        tm_date = "%s%s" %(date, cur_time_d) #Create time and date string
        
        if chosen_body[0] == "Sun":
            body = ephem.Sun()
            body.compute(tm_date, epoch=date)
            obj_ra = float(body.a_ra)*_rad_to_deg
            obj_dec = float(body.a_dec)*_rad_to_deg
        elif chosen_body[0] == "Moon":
            body = ephem.Moon()
            body.compute(tm_date, epoch=date)
            obj_ra = float(body.a_ra)*_rad_to_deg
            obj_dec = float(body.a_dec)*_rad_to_deg
        elif chosen_body[0] == "Jupiter":
            body = ephem.Jupiter()
            body.compute(tm_date, epoch=date)
            obj_ra = float(body.a_ra)*_rad_to_deg
            obj_dec = float(body.a_dec)*_rad_to_deg
        else:
            obj_ra = float(chosen_body[1])
            obj_dec = float(chosen_body[2])

        if chosen_body[1] == -1: #When the object is not stationary, execute the following
            sum_ra = sum_dec = 0 #Initialize the sum holding variables
            for i in range(0, 60):
                #cur_time_d += 6.9444444444444445e-04 #Add a minute each time, because a change in seconds is too small
                cur_time_d += 0.0416666666666667 #Add an hour in each iteration, because the change in time for RA/DEC is small
                tm_date = "%s%s" %(date, cur_time_d) #Create the date and time string to use it for the calculations
                body.compute(tm_date, epoch=date) #Compute the RA and DEC for the current date and time
                cur_ra = float(body.a_ra) #Calculated RA for the body
                cur_dec = float(body.a_dec) #Calculated DEC for the body
                if i > 0:
                    #Take the sum of each value to calculate average later
                    sum_ra += (cur_ra - prev_ra)
                    sum_dec += (cur_dec - prev_dec)
                prev_ra = cur_ra #Set the previous value to the current one before reiterating
                prev_dec = cur_dec #Set the previous value to the current one before reiterating
            roc_ra = ((sum_ra/59)*_rad_to_deg)*3600 #Mean rate of change for the RA in arcsec/hour
            roc_dec = ((sum_dec/59)*_rad_to_deg)*3600 #Mean rate of change for the DEC in arcsec/hour
        else:
            roc_ra = roc_dec = 0 #If the body is stationary (RA/DEC does not change with time), then set the rate of change to zero
        
        ans = input("\nDo you want to start tracking? Enter 'y' for yes or anything to quit tracking: ")
        if ans == "y":
            #Get the current dish position in steps to use in further calculations
            pos = self.clientSocket.sendRequest("Report Position")
            stp_deg = self.clientSocket.sendRequest("SCALE")
            if pos == "No answer" or stp_deg == "No answer":
                print("There was problem contacting the server to get the position. Returning to control menu.")
                self.logdata.log("WARNING", "There was problem contacting the server to get the position", "trackingMenu")
                return 1 #Return to control menu
            else:
                tmp_pos = pos.split("_")
                tmp_stp = stp_deg.split("_")
                cur_stp_ra = float(tmp_pos[3]) #Current position of motor away from home on RA axis
                cur_stp_dec = float(tmp_pos[4]) #Current position of the motor away from home on DEC axis
                
                #Number of steps per degree for the current motors
                stpp_deg_ra = int(tmp_stp[2])
                stpp_deg_dec = int(tmp_stp[4])
            
            #If the dish is taking considerable time to got to position, we will set the position accordingly
            #By adding the required amount of time on the hour angle above (by changing the tm_date string)
            #Call the transit first to set the dish to a position ahead of the target and wait until it passes in front of the dish
            #After coming in the dish center, then start tracking
            t_obj = time.gmtime() #Get the return from the gmtime function to use it in the date creation
            cur_time_d = float(t_obj.tm_mday) + float(t_obj.tm_hour)/24.0 + float(t_obj.tm_min/1440.0) + float(t_obj.tm_sec/86400.0)
            tm_date = "%s%s" %(date, cur_time_d) #Create time and date string and add the required amount of time to set the dish position
            
            #The hour angle of the object is LST (Local Sidereal Time) - a (Right Ascension)
            self.observer.date = tm_date #Set the observer's date
            hour_ang = float(self.observer.sidereal_time())*_rad_to_deg - obj_ra #ephem sidereal returns in rad
            
            start_time = 5 #Start tracking five seconds after the position setting
            
            #Max speed is 400Hz or 400stp/sec
            #srat_time is the time duration after which the tracking starts
            tim_ra = ((((hour_ang*stpp_deg_ra + cur_stp_ra)/400) + start_time)/3600)*15 #Convert to hours by 3600 and then to deg by 15
            tim_dec = ((((obj_dec*stpp_deg_dec + cur_stp_dec)/400) + start_time)/3600)*15
            if tim_ra > tim_dec:
                hour_ang += tim_ra #Change the hour angle according to the value
                obj_ra += (tim_ra/15)*(roc_ra/3600) #Calculate the RA based on the ROC for the time passed
                obj_dec += (tim_dec/15)*(roc_dec/3600) #Calculate the DEC based on the ROC for the time passed
            else:
                hour_ang += tim_dec
                obj_ra += (tim_ra/15)*(roc_ra/3600)
                obj_dec += (tim_dec/15)*(roc_dec/3600)
            
            #Add control for the negative value of the hour angle
            #When the hour angle is negative then add 360 to make it positive if you wish, or indicate leftward direction, provided that the 0 position is south
            self.logdata.log("INFO", "Transit command sent\nObject: %s\nSidereal Time: %.5f\nRA: %.5f\nDEC: %.5f\nHour angle: %.5f" 
                %(chosen_body[0], float(self.observer.sidereal_time())*_rad_to_deg, obj_ra, obj_dec, hour_ang), "trackingMenu")
            
            #Send the transit request for the current object and that is done to set the dish position for tracking
            rsp = self.clientSocket.sendRequest("TRNST_RA_%.5f_DEC_%.5f" %(hour_ang, obj_dec)) #Send the transit request and get the response
            if rsp == "No answer":
                rsp = self.clientSocket.longWait_rcv(60) #Wait to receive the response for 60 seconds, because the dish can take time to reach position
            elif rsp == "POSITION_SET":
                print("The telescope is ready to start tracking.")
                self.logdata.log("INFO", "The telescope is at its position and ready to start tracking.", "trackingMenu")
            else:
                print("There was a problem with setting the telescopes position. %s" %rsp)
                self.logdata.log("WARNING", "There was a problem with setting the telescopes position. Server sent: %s" %rsp, "trackingMenu")
                sleep(3) #Stop so the user sees the message
                return 1 #Return to control menu
            
            #Send the command and get the response
            response = self.clientSocket.sendRequest("AAF_RA_%.5f_ROC_%f_DEC_%.5f_ROC_%f_TIM_%f_STRT_%f" 
                %(obj_ra, roc_ra, obj_dec, roc_dec, float(track_time), start_time))
            
            self.logdata.log("INFO", 
                "Aim and Follow command was sent with the following details\nObject name: %s\nRA/ROC: %.5f/%.5f\nDEC/ROC: %.5f/%.5f\nStart time: %d" 
                %(chosen_body[0], obj_ra, roc_ra, obj_dec, roc_dec, int(start_time)), "trackingMenu")
            print("AAF_RA_%.5f_ROC_%f_DEC_%.5f_ROC_%f_TIM_%f" %(obj_ra, roc_ra, obj_dec, roc_dec, float(track_time))) #Debugging purposes
        else:
            return 1 #Return to control menu
        #Add more control
        if response == "OBJECT_CENTERED_TRACKING_STARTED":
            print("Tracking successfully started.")
            self.logdata.log("INFO", "Telescope successfully tracking the requested object.", "trackingMenu")
        else:
            print("There was a problem with the tracking, try again or fix the problem.")
            self.logdata.log("WARNING", "There was a problem with object tracking and the telescope is not tracking. Server sent: %s" 
                %response, "trackingMenu")
        sleep(3) #Pause some time, so the user can see the messages
        
    #def scanningMenu(self):
        
    
    #def skyscanMenu(self):
        
    
    def objectMenu(self):
        #Add functionality to choose objects from a catalog
        while(True):
            self.cls() #Clear the previous menu before showing the new one
            chosen_body = self.cfgData.getObject() #Get the currently chosen object
            
            print("***********************************************")
            print("   [*]Selected object:")
            if chosen_body[1] == -1:
                print("         >Name: %s" %chosen_body[0])
            else:
                print("         >Name: %s" %chosen_body[0])
                print("         >RA :  %s" %chosen_body[1] + u"\u00b0")
                print("         >DEC:  %s" %chosen_body[2] + u"\u00b0")
            print("***********************************************")
            
            showMenu().object()
            choice = input("Enter your menu choice: ")
            
            if choice == "1":
                self.cfgData.setObject("Sun")
            elif choice == "2":
                self.cfgData.setObject("Moon")
            elif choice == "3":
                self.cfgData.setObject("Jupiter")
            elif choice == "4":
                self.cls()
                print("Enter the object details below.")
                name_in = input("Object's name: ")
                ra_in = input("Right Ascension (RA): ")
                dec_in = input("Declination (DEC): ")
                #Type conversion is needed for the coordinates before saving
                self.cfgData.setObject(name_in, ra_in, dec_in)
            elif choice == "5":
                break
    
    def positionMenu(self):
        while(True):
            self.cls() #Clear the previous menu items
            cur_pos = self.clientSocket.sendRequest("Report Position") #Take the position of the radio telescope
            if (cur_pos == "No answer") or (cur_pos == None):
                print("Can not get the current position of the system.")
                self.logdata.log("ERROR", "Can not get the current position of the system.", "positionMenu")
            else:
                cur_pos = cur_pos.split("_")
                print("The current position of the radio telescope is:")
                self.logdata.log("INFO", "The current telescope position is\nRA: %s\nDEC: %s" %(cur_pos[1], cur_pos[2]), "positionMenu")
                if cur_pos[0] == "POS":
                    #Make the formatting according to the data sent from the radio telescope pi
                    print("  >RA : %s" %cur_pos[1] + u"\u00b0")
                    print("  >DEC: %s" %cur_pos[2] + u"\u00b0\n")
            user_inp = input("Press enter to return to main menu: ") #Prompt the user to return to main menu
            while(user_inp != ""):
                user_inp = input("Please press enter if you want to return to main menu: ")
            break #Return to main menu after a successful run
    
    def getAngle(self, angName):
        print("\nEnter the " + angName + " in decimal degrees.")
        print("For a south Latitude or a western Longitude, enter a minus sign in the decimal value.")
        return input(angName + ": ") #Return the angle entered by the user
    
    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear') #Clear command to work in windows 'nt' and Linux
        showMenu().intro() #After clearing the screen show the intro in each call