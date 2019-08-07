# python 2.7

import RSA
from SocketServer import BaseRequestHandler,ThreadingTCPServer
import threading
import hashlib
import crypto

BUF_SIZE=1024

class Handler(BaseRequestHandler):
    def handle(self):
        global key
        global public_key
        global private_key
        address,pid = self.client_address
        print('%s connected!'%address)
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data)>0:
                print('receive=',data.decode('utf-8'))
                cur_thread = threading.current_thread()
                hdata=crypto.md5(data)
                print (hdata)
                response = RSA.encrypt(hdata,private_key)+'/'+public_key
                self.request.sendall(response)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8998
    ADDR = (HOST,PORT)
    key=RSA.Build_key('CA') # CA build public and private key
    public_key = key.split('/')[0]+'/'+key.split('/')[1] # n/e pair
    private_key = key.split('/')[0]+'/'+key.split('/')[2] # n/d pair
    server = ThreadingTCPServer(ADDR,Handler)  
    print('Listening Client Application')
    server.serve_forever()  
    print(server)
