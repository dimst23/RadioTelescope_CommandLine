import socket

class TCPClient(object):
    def __init__(self, cfgData):
        self.conf = cfgData
        self.sock_exst = False #Indicate that a socket does not object exist
        self.sock_connected = False #Indicate that there is currently no connection
        self.sock = self.createSocket()
        autocon = cfgData.getTCPAutoConnStatus() #See if autoconnection at startup is enabled
        if autocon == "yes":
            host = cfgData.getHost()
            port = cfgData.getPort()
            self.connect(host, port)
    
    def createSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket object
        sock.settimeout(20) #Set the timeout to 20 seconds
        self.sock_exst = True #Indicate that a socket object exists
        return sock
    
    def connect(self, host, port):
        if self.sock_exst == False:
            self.sock = self.createSocket()
        try:
            self.sock.connect((host, int(port)))
            self.sock_connected = True
        except:
            self.sock_connected = False
        return self.sock_connected
    
    def disconnect(self):
        if self.sock_exst and self.sock_connected:
            self.sock.close()
            self.sock_exst = False
            self.sock_connected = False
        else:
            self.sock_connected = False
        return self.sock_connected
    
    def sendRequest(self, request):
        if self.sock_connected:
            try:
                self.sock.send(request.encode('utf-8'))
                response = self.sock.recv(1024).decode('utf-8')
                return response
            except:
                return "No answer"