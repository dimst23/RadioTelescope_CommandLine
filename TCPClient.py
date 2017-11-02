import socket

class TCPClient(object):
	def __init__(self, cfgData):
		self.conf = cfgData
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock_exst = True
		autocon = cfgData.getTCPAutoConnStatus()
		if autocon == "yes":
			host = cfgData.getHost()
			port = cfgData.getPort()
			self.connect(host, port)
			
	def connect(self, host, port):
		if self.sock_exst == False:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock_exst = True
		try:
			self.sock.connect((host, port))
			self.sock_connected = True
		except:
			self.sock_connected = False
		return self.sock.connected
	
	def disconnect(self):
		if self.sock_exst and self.sock_connected:
			self.sock.close()
			self.sock_exst = False
			self.sock_connected = False
		else:
			self.sock_connected = False
	
	def sendRequest(self, request):
		if self.sock.connected:
			self.sock.send(request.encode('utf-8'))
			return self.sock.recv(1024).decode('utf-8')
	
	