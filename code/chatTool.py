# python 2.7
# import everything we need.
import wx
import socket
import thread
import sys
import select
import Queue
import RSA
import crypto
sys.setrecursionlimit(100000)

#adjust certificate and get ca_public_key
def get_certificate_ca_public(info,clientid):
      global ca_public_key,certificate
      certificate = public_key + '/' +clientid+'/'+ info.split('/')[0]
      ca_public_key = info.split('/')[1]+'/'+info.split('/')[2]
      return certificate

# apply certificates
def connectCA(pub_key,clientid):
        
        HOST = '127.0.0.1'
        PORT = 8998
        ADDR =(HOST,PORT)
        BUFSIZE = 1024
        sock = socket.socket()
        
        sock.connect(ADDR)
        print('Have connected with Certificate Authority')

        while True:
              appInfo= pub_key + '/' + clientid
             
              if len(appInfo)>0:
                 print('send:',appInfo)
                 sock.sendall(appInfo.encode('utf-8')) 
                 recv_data = sock.recv(BUFSIZE)
                 certificate=get_certificate_ca_public(recv_data,clientid)
                 print('certificate:',certificate)
                 sock.close()
                 break
def modifymessage(meg):
	
	return meg[0:2]+'11001100'+meg[10:]
def ifmasAttack():
    global private_key,public_key
    if masMark==0:
        public_key = key.split('/')[0]+'/'+key.split('/')[1] # n/e pair
        private_key = key.split('/')[0]+'/'+key.split('/')[2] # n/d pair
    else:
        public_key = masKey.split('/')[0]+'/'+key.split('/')[1] # n/e pair
        private_key = masKey.split('/')[0]+'/'+key.split('/')[2] # n/d pair
class chatdlg(wx.Dialog):
	
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'Chat Tool', 
                size=(850, 460))

        self.DisplayText = wx.TextCtrl(self, -1, '', 
                size=(500, 350), style=wx.TE_MULTILINE)

        self.InputText = wx.TextCtrl(self, -1, "Nihao,Hi,Konnichiwa", 
                pos=(5, 370), size=(500, -1))

        self.sendButton = wx.Button(self, -1, "Send", pos=(540, 370))
        self.Bind(wx.EVT_BUTTON, self.OnSendClick, self.sendButton)
        self.sendButton.SetDefault()

        wx.StaticText(self, -1, "IP", (505, 30))
        self.IPText = wx.TextCtrl(self, -1, "127.0.0.1", 
                pos=(540, 30), size=(150, -1))
        wx.StaticText(self, -1, "Port", (700, 30))
        self.PortText = wx.TextCtrl(self, -1, "8001", 
                pos=(730, 30), size=(50, -1))
        
        wx.StaticText(self, -1, "Guide:", (505, 80))
        wx.StaticText(self,-1,'Step 1: Input your name & Select your role',(550, 80))
        wx.StaticText(self,-1,'Step 2: Client needs apply certificate on CA',(550, 100)) 
        wx.StaticText(self,-1,'Step 3: Clients need exchange their certificate\n '+'before send data',(550, 120))       
        wx.StaticText(self,-1,'Step 4: You can send data by now',(550, 160)) 
        #self.IPText = wx.TextCtrl(self, -1, guide, 
                #pos=(540, 80), size=(250, 100))

        #Client botten
        self.InputText1 = wx.TextCtrl(self, -1, "ClientName", 
                pos=(540, 250), size=(100, -1))
        self.cButton = wx.Button(self, -1, "I am a Client", pos=(540, 200))
        self.Bind(wx.EVT_BUTTON, self.OnClientClick, self.cButton)
        # Server botten
        self.InputText2 = wx.TextCtrl(self, -1, "ServerName", 
                pos=(680, 250), size=(100, -1))
        self.sButton = wx.Button(self, -1, "I am the Server", pos=(680, 200))
        self.Bind(wx.EVT_BUTTON, self.OnSeverClick, self.sButton)
        
        #apply certificate butten
        self.authButton = wx.Button(self, -1, "Apply certificate", pos=(540, 300))
        self.Bind(wx.EVT_BUTTON, self.OnApplyClick, self.authButton)
        #exchange certificate butten
        self.exchangeCertButton = wx.Button(self, -1, "Exchange Certificate", pos=(680, 300))
        self.Bind(wx.EVT_BUTTON, self.OnExchangeClick, self.exchangeCertButton)
        # modification method
        self.cb1 = wx.CheckBox(self, label = 'Modification Attack',pos = (670,370)) 
        self.Bind(wx.EVT_CHECKBOX,self.onModificationChecked,self.cb1)
        # show cipher
        self.cb2 = wx.CheckBox(self, label = 'Show cipher',pos = (670,390)) 
        self.Bind(wx.EVT_CHECKBOX,self.showCipher,self.cb2)
        # pretender
        self.cb3 = wx.CheckBox(self, label = 'Masquerade Attack',pos = (670,350)) 
        self.Bind(wx.EVT_CHECKBOX,self.Masquerader,self.cb3)

    # click send 
    def OnSendClick(self, event):
        global key,cipherMark
        global public_key,private_key,peer_public
        ifmasAttack()
        self.plaintext=self.InputText.GetValue()
        self.send_data = crypto.encryptData(self.plaintext,private_key,peer_public)
        try:
            self.client.send(self.send_data)
            self.DisplayText.AppendText('\nYour Text:  [')
            self.DisplayText.AppendText(self.plaintext)
            self.DisplayText.AppendText(']\n')
            if cipherMark==1:
               self.DisplayText.AppendText('\nYour cipher:  [')
               self.DisplayText.AppendText(self.send_data)
               self.DisplayText.AppendText(']\n')
        except  socket.error,e:
            self.DisplayText.AppendText('Pls connect to chat server @%d firstly\n' % self.port)

    def OnApplyClick(self,event):
    	global public_key,private_key
    	global key
    	#public_key = key.split('/')[0]+'/'+key.split('/')[1] # n/e pair
    	#private_key = key.split('/')[0]+'/'+key.split('/')[2] # n/d pair
    	#appInfo= public_key + '/' +self.clientname
    	try:
            connectCA(public_key,self.clientname)
    	    self.DisplayText.AppendText('\n  [')
    	    self.DisplayText.AppendText('You got certificate')
            self.DisplayText.AppendText(']\n')
        except  socket.error, e:
            self.DisplayText.AppendText('get certificate failed\n' )

    def OnExchangeClick(self ,event):
    	global key
        global public_key,private_key,certificate

        self.send_data = 'cEr'+'/'+certificate
        print self.send_data
        try:
            self.client.send(self.send_data)
            self.DisplayText.AppendText('\n  [')
            self.DisplayText.AppendText('certificate is sent')
            self.DisplayText.AppendText(']\n')
        except  socket.error, e:
            self.DisplayText.AppendText('exchange certificate failed\n')

    def onModificationChecked(self,event):
    	global mark
        mark = 1-mark

    def showCipher(self,event):
    	global cipherMark
    	cipherMark = 1-cipherMark
    
    def Masquerader(self,event):
        global masMark
        masMark = 1-masMark
    def SocketProc_server(self):
        #self.sButton.SetLabel(self.PortText.GetValue())
        self.sButton.SetLabel('Server Model')
        # Sockets to which we expect to write
        outputs = [ ]

        # Outgoing message queues (socket:Queue)
        message_queues = {}

        # creat socket and bind
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.port = int(self.PortText.GetValue())
        self.host = ''

        print 'Waiting for connection @%s:%d\n' % (self.host, self.port)

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)        

        self.DisplayText.AppendText('Waiting for connection @%s:%d\n' % (self.host, self.port))
        
        # Sockets from which we expect to read
        inputs = [ self.server ]

        while inputs:
            # Wait for at least one of the sockets to be ready for processing
            print >>sys.stderr, '\nwaiting for the next event'
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            
            # Handle inputs
            for s in readable:
                if s is self.server:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print >>sys.stderr, 'new connection from', client_address
                    self.DisplayText.AppendText('new connection from %s %s\n' % client_address)
                    connection.setblocking(False)
                    inputs.append(connection)

                    # Give the connection a queue for data we want to send
                    message_queues[connection] = Queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        # A readable client socket has data
                        print >>sys.stderr, '\nreceived [%s] from %s' % (data, s.getpeername())

                        self.DisplayText.AppendText('received [%s] from %s\n' % (data, s.getpeername()))

                        for c in inputs:
                            if c is self.server:
                                print >>sys.stderr, 'from server'
                            elif c is not s:
                                print >>sys.stderr, 'send_data [%s] to %s' % (data, s.getpeername())
                                message_queues[c].put('[' + data + '] from'+str(s.getpeername()))
                                if c not in outputs:
                                    outputs.append(c)
                    else:   
                        # Interpret empty result as closed connection
                        #print >>sys.stderr, 'closing', client_address, 'after reading no data'

                        self.DisplayText.AppendText('closing %s %s after reading no data\n\n' % client_address)
                        # Stop listening for input on the connection
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        
                        # Remove message queue
                        del message_queues[s]

            # Handle outputs
            for s in writable:
                try:
                    next_msg = message_queues[s].get_nowait()
                except Queue.Empty:
                    # No messages waiting so stop checking for writability.
                    print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
                    outputs.remove(s)
                else:
                    print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
                    if mark==1:
                       next_msg=modifymessage(next_msg)
                       self.DisplayText.AppendText('\nmessage is modified to: %s' % (next_msg))
                    s.send(next_msg)
            # Handle "exceptional conditions"
            for s in exceptional:
                print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
                self.DisplayText.AppendText('handling exceptional condition for', s.getpeername())
                # Stop listening for input on the connection
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]   

    def SocketProc_client(self):
        #self.cButton.SetLabel(self.PortText.GetValue())
        self.cButton.SetLabel('Client Model')
        # Sockets to which we expect to write
        outputs = [ ]

        # Outgoing message queues (socket:Queue)
        message_queues = {}

        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host = str(self.IPText.GetValue())
        self.port = int(self.PortText.GetValue())
        print 'Connecting to chat server@%s:%d\n' % (self.host, self.port)
        try:
            self.client.connect((self.host, self.port))
            print 'connected to chat server @%s:%d\n' % (self.host, self.port)
            self.DisplayText.AppendText('Connected to chat server@%s:%d\n' % (self.host, self.port))
        except socket.error, e:
            print 'Could not connect to chat server @%s:%d\n' % (self.host, self.port)
            self.DisplayText.AppendText('Could not connect to chat server @%s:%d\n' % (self.host, self.port))
            return

        inputs = [ self.client ]
        message_queues[self.client] = Queue.Queue()

        while inputs:
            # Wait for at least one of the sockets to be ready for processing
            print >>sys.stderr, '\nwaiting for the next event'
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            
            # Handle inputs
            for s in readable:
                data = s.recv(1024)
                if data:
                    # A readable client socket has data
                    data=data.split("]")
                    data= data[0].lstrip('[')
                    global peer_public
                    if data.split('/')[0] == 'cEr':
                    	peer_certificate1=data.split('/')[1]+'/'+data.split('/')[2]+'/'+data.split('/')[3]
                        peer_public = data.split('/')[1]+'/'+data.split('/')[2]
                    	hcertificate=RSA.decrypt(data.split('/')[4],ca_public_key)
                    	if crypto.md5(peer_certificate1)==hcertificate:
                    	     self.DisplayText.AppendText('\ncertificate receiveded\n')	
                    	else:
               
                    		self.DisplayText.AppendText('exchange certificate failed\n')
                    else:
                       Text=crypto.decryptData(data,private_key,peer_public)
                       #print data
                       print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                       global cipherMark
                       if cipherMark==1:
                           self.DisplayText.AppendText('\nreceived cipher: "%s"\n' % data)
                       self.DisplayText.AppendText('\nreceived text:"%s"\n' % Text)
                       #if data=='esc': self.client.close()
                       #self.DisplayText.AppendText('esc\n' )
                else:
                    # Interpret empty result as closed connection
                    print >>sys.stderr, 'closing', client_address, 'after reading no data'

                    self.DisplayText.AppendText('closing %s %s after reading no data\n\n' % client_address)
                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    
                    # Remove message queue
                    del message_queues[s]

            # Handle outputs
            for s in writable:
                try:
                    next_msg = message_queues[s].get_nowait()
                except Queue.Empty:
                    # No messages waiting so stop checking for writability.
                    print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
                    outputs.remove(s)
                else:
                    print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
                    s.send(next_msg)
            # Handle "exceptional conditions"
            for s in exceptional:
                print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
                self.DisplayText.AppendText('handling exceptional condition for', s.getpeername())
                # Stop listening for input on the connection
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]    
    

    def OnSeverClick(self, event):
        global key
        self.servername=self.InputText2.GetValue()
        self.socketmode=1
        #self.sButton.SetLabel("Server")
        key=RSA.Build_key(self.servername)
        print key
        thread.start_new_thread(self.SocketProc_server,())

    def OnClientClick(self, event):
        global key,masKey,public_key,private_key
        self.clientname=self.InputText1.GetValue()
        self.socketmode=0
        #self.cButton.SetLabel("Client")
        key=RSA.Build_key(self.clientname)
        masKey=RSA.Build_key(self.clientname)#Masquerader attack test
        public_key = key.split('/')[0]+'/'+key.split('/')[1] # n/e pair
        private_key = key.split('/')[0]+'/'+key.split('/')[2] # n/d pair
        thread.start_new_thread(self.SocketProc_client,())



if __name__ == '__main__':
    mark=0
    masMark=0
    cipherMark=0
    app = wx.App()
    app.MainLoop() 
    dialog = chatdlg()
    result = dialog.ShowModal()
    if result == wx.ID_OK:
        print "OK"
    else:
        print "Cancel"
    dialog.Destroy()