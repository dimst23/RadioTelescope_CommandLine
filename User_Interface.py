#Import the required libraries
import os
import ephem
import time
import logData
from showMenu import showMenu
from time import sleep

_rad_to_deg = 57.2957795131

#General Notes
'''
   Include returning to home position when closing the program 
'''


class uInterface(object):
    def __init__(self, cfgData, clientSocket):
        self.clientSocket = clientSocket
        self.cfgData = cfgData
        self.observer = ephem.Observer()
        self.logdata = logData.logData(__name__)
        self.mainMenu()
    
    def mainMenu(self):
        while(True):
            lalon = self.cfgData.getLatLon()
            self.observer.lon, self.observer.lat = lalon[1], lalon[0] #Set the observer location according to the saved settings
            print("Getting TCP connection status...")
            conStatus = self.clientSocket.sendRequest("Test") #Get the connection status
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
                print("         >RA:   %s" %cur_obj[1])
                print("         >DEC:  %s" %cur_obj[2])
            print("***********************************************")
            
            #Show the correct menu according to the connection status with the server
            if conStatus == "OK":
                showMenu().main_con() #Show the main menu items
                choice = input("Enter your menu choice: ")
                
                if choice == "1":
                    self.positionMenu()
                elif choice == "2":
                    self.objectMenu()
                elif choice == "3":
                    #self.controlMenu()
                    self.transitMenu()
                    #self.trackingMenu()
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
                    self.clientSocket.disconnect()
                    self.logdata.logClose()
                    print("\nGoodbye! See you again later!")
                    sleep(2)
                    break #Terminate the program
            else:
                showMenu().main_nocon()
                choice = input("Enter your menu choice: ")
                
                if choice == "1":
                    self.objectMenu()
                elif choice == "2":
                    self.TCPMenu()
                elif choice == "3":
                    self.locationMenu()
                elif choice == "4":
                    #Additional code may be added if some other processes are active, to terminate them
                    self.logdata.logClose()
                    print("\nGoodbye! See you again later!")
                    sleep(2)
                    break #Terminate the program

    def locationMenu(self):
        wrong_ch = False #Indicate if there is a wrong choice input from the user
        
        s_latlon = self.cfgData.getLatLon() #First element is latitude and second element is longitude
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
                        self.observer.lat, self.observer.lon = s_latlon[0], s_latlon[1]
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
                    And the values are going to be changed.
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
                            self.logdata.log("INFO", "TCP disconnected from server.", "TCPMenu")
                            serv_change = True
                        else:
                            print("Couldn\'t terminate properly, but the new settings will be saved.")
                            self.logdata.log("WARNING", "Couldn\'t terminate properly, but the new settings will be saved.", "TCPMenu")
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
                            print("Successfully connected with the server.")
                        else:
                            print("There was a communication problem with the server.")
                            self.logdata.log("WARNING", "There was a communication problem with the server.", "TCPMenu")
                    sleep(1) #Pause for one second so the message is visible
                continue #Stay in the TCP menu
                
            elif choice == "2":
                print("\nTrying to connect to the server.")
                print("The details of the server are %s:%s" %(s_host, s_port))
                conStatus = self.clientSocket.sendRequest("Test")
                
                #Output messages according to the previous result of connection status
                if conStatus == "OK":
                    print("\nSuccesfully contacted the server.")
                else:
                    print("\nUnfortunately, communication with the server was impossible.")
                    self.logdata.log("WARNING", "Unfortunately, communication with the server was impossible.", "TCPMenu")
                sleep(2) #Keep the message for two seconds
                
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
                    print("\nConnecting to server %s:%s\n" %(s_host, s_port))
                    if self.clientSocket.connect(s_host, s_port):
                        contct = self.clientSocket.sendRequest("Test") #Try to make a contact with the server
                        if contct == "OK": #If contact was made, print the following
                            print("Successfully connected to the server %s:%s" %(s_host, s_port))
                            print("And also made contact with the server.")
                    else:
                        print("Failed to connect to the server %s:%s" %(s_host, s_port))
                        self.logdata.log("WARNING", "Failed to connect to the server %s:%s" %(s_host, s_port), "TCPMenu")
                    sleep(2)
            
            #Choice No.5 will be available if an only if the client is not connected to the server
            elif (choice == "5") and (conStatus != "OK"):
                break #Return to main menu
            else:
                wrong_ch = True #Reiterate. Show the appropriate message to the user

    def transitMenu(self):
        obj_ra = "-1"
        obj_dec = "-1"
        man_ra = "-1"
        man_dec = "-1"
        
        while(True):
            chosen_body = self.cfgData.getObject() #Get the currently chosen object
            self.cls() #Clear the previous menu before showing the new one
            print("***********************************************")
            
            print("   [*]Selected object:")
            if chosen_body[1] == -1:
                print("         >Name: %s" %chosen_body[0])
            else:
                print("         >Name: %s" %chosen_body[0])
                print("         >RA:   %s" %chosen_body[1])
                print("         >DEC:  %s" %chosen_body[2])
            print("***********************************************")
            showMenu().transit()
            choice = input("Enter your menu choice: ")
            
            if choice == "1":
                self.cls()
                print("Give a transit time, in 24hr format, which is after the time that enter will be pressed (at least 1 minute).")
                print("For better results, provide a time at least 10 minutes from the current time.")
                tim = input("Give the transit time in UTC by separating hours, minutes, seconds with ':' (e.g. '20:12:34'): ")
                
                '''
                    Get the time from the user and then check if it is the same as the current time.
                    If it is then inform the user and ask for another entry.
                    If the time is good, then proceed by taking the current date and combining it with the given time in a string.
                    The above string will be used as an input to calculate the ephemeris data of the non stationary bodies.
                    time.gmtime(), tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec
                '''
                t_obj = time.gmtime() #Get the return from the gmtime function to use it in the date creation
                while(True):
                    temp = tim.split(":")
                    if int(temp[0]) < 24 or int(temp[1]) <= 59 or int(temp[2]) <= 59:
                        if int(temp[0]) > int(t_obj.tm_hour) or ((int(t_obj.tm_hour) == int(temp[0])) 
                            and (int(t_obj.tm_min) - (int(temp[1])) is not 0) and (int(temp[1]) > int(t_obj.tm_min))):
                            break
                        else:
                            tim = input("Please enter a correct time: ")
                
                #If everything succeeds from the control, then move on with the following
                date = "%s/%s/%s" %(t_obj.tm_year, t_obj.tm_mon, t_obj.tm_mday) #Save the date in a string in the appropriate format
                eph_t_date = "%s %s" %(date, tim) #Make the correct date time string to be used to calculated ephemeris
                
                if chosen_body[0] == "Sun":
                    sun = ephem.Sun()
                    sun.compute(eph_t_date, epoch=date) #Calculate ephemeris at the current date
                    obj_ra = float(sun.a_ra)*_rad_to_deg
                    obj_dec = float(sun.a_dec)*_rad_to_deg
                elif chosen_body[0] == "Moon":
                    moon = ephem.Moon()
                    moon.compute(eph_t_date, epoch=date) #Calculate ephemeris at the current date
                    obj_ra = float(moon.a_ra)*_rad_to_deg
                    obj_dec = float(moon.a_dec)*_rad_to_deg
                elif chosen_body[0] == "Jupiter":
                    jup = ephem.Jupiter()
                    jup.compute(eph_t_date, epoch=date) #Calculate ephemeris at the current date
                    obj_ra = float(jup.a_ra)*_rad_to_deg
                    obj_dec = float(jup.a_dec)*_rad_to_deg
                else:
                #Add control to what to do with stationary bodies
                    obj_ra = float(chosen_body[1])
                    obj_dec = float(chosen_body[2])
                #The hour angle of the object is LST (Local Sidereal Time) - a (Right Ascension)
                self.observer.date = eph_t_date
                hour_ang = float(self.observer.sidereal_time())*_rad_to_deg - obj_ra #ephem sidereal returns in rad
                #Add control for the negative value of the hour angle
                #When the hour angle is negative then add 360 to make it positive if you wish, or indicate leftward direction, provided that the 0 position is south
                self.logdata.log("INFO", "Transit command sent\nObject: %s\nSidereal Time: %s\nRA: %s\nDEC: %s\nThe hour angle: %s" 
                    %(chosen_body[0], float(self.observer.sidereal_time())*_rad_to_deg, obj_ra, obj_dec, hour_ang), "transitMenu")
                #sleep(5) #Used for testing
                
                #Send the request for the transit along with the required information to the Raspberry Pi
                rsp = self.clientSocket.sendRequest("TRNST_RA_%s_DEC_%s" %(hour_ang, obj_dec)) #Send the transit request and get the response
                if rsp == "No answer":
                    rsp = self.clientSocket.longWait_rcv(60) #Wait to receive the response for 60 seconds, because the dish can take time to reach position
                
                if rsp == "POSITION_SET":
                    print("The telescope is at its position for transit.")
                    self.logdata.log("INFO", "The telescope is at its position for transit.", "transitMenu")
                else:
                    print("There was a problem with setting the telescopes position. %s" %rsp)
                    self.logdata.log("WARNING", "There was a problem with setting the telescopes position. Server sent: %s" %rsp, "transitMenu")
                
            elif choice == "2":
                break

    #def controlMenu(self):
        #Show the currently chosen object
        #Show if the telescope is now tracking or not (check that by asking the appropriate command through the TCP)
        #Show the current position of the telescope if not tracking (use the appropriate command to get the dish's position)
    
    def trackingMenu(self):
        chosen_body = self.cfgData.getObject() #Get the currently chosen object
        self.cls()
        print("***********************************************")
        print("   [*]Selected object:")
        if chosen_body[1] == -1:
            print("         >Name: %s" %chosen_body[0])
        else:
            print("         >Name: %s" %chosen_body[0])
            print("         >RA:   %s" %chosen_body[1])
            print("         >DEC:  %s" %chosen_body[2])
        print("***********************************************")
        
        print("Tracking Menu")
        track_time = input("Enter for how long you want the object to be tracked in seconds: ")
        
        t_obj = time.gmtime() #Get the return from the gmtime function to use it in the date creation
        date = "%s/%s/" %(t_obj.tm_year, t_obj.tm_mon) #Save the date in a string in the appropriate format
        cur_time_d = float(t_obj.tm_mday) + float(t_obj.tm_hour)/24.0 + float(t_obj.tm_min/60.0) + float(t_obj.tm_sec/3600.0)
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
                tm_date = "%s%s" %(date, cur_time_d)
                body.compute(tm_date, epoch=date)
                cur_ra = float(body.a_ra)
                cur_dec = float(body.a_dec)
                if i > 0:
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
            #Send the command and get the response
            response = self.clientSocket.sendRequest("AAF_RA_%f_ROC_%f_DEC_%f_ROC_%f_TIM_%f" %(obj_ra, roc_ra, obj_dec, roc_dec, float(track_time)))
            print("AAF_RA_%f_ROC_%f_DEC_%f_ROC_%f_TIM_%f" %(obj_ra, roc_ra, obj_dec, roc_dec, float(track_time)))
            sleep(3)
        else:
            return 1
        #Add more control
        if response == "AIM_CENTERED_TRK_STARTED":
            print("Tracking successfully started.")
            sleep(3)
        else:
            print("There was a problem with the tracking, try again or fix the problem.")
        
    #def scanningMenu(self):
        
    
    #def skyscanMenu(self):
        
    
    def objectMenu(self):
        #Add functionality to choose objects from a catalog
        while(True):
            self.cls() #Clear the previous menu before showing the new one
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
                ra_in = input("Right Ascension: ")
                dec_in = input("Declination: ")
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
                self.logdata.log("ERROR", "Can not get the current position of the system.")
            else:
                cur_pos = cur_pos.split("_")
                print("The current position of the radio telescope is:")
                if cur_pos[0] == "POS":
                    #Make the formatting according to the data sent from the radio telescope pi
                    print("  >RA : %s" %cur_pos[1])
                    print("  >DEC: %s\n" %cur_pos[2])
            user_inp = input("Type 1 to return to main menu: ") #Prompt the user to return to main menu
            while(user_inp != "1"):
                user_inp = input("Please enter 1 if you want to return to main menu: ")
            break #Return to main menu after a successful run
    
    def getAngle(self, angName):
        print("\nEnter the " + angName + " in decimal degrees.")
        print("For a south Latitude or a weste Longitude, enter a minus sign in the decimal value.")
        return input(angName + ": ") #Return the angle entered by the user
    
    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        showMenu().intro()