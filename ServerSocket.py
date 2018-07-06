#!/usr/bin/env python
from socket import socket,AF_INET,SOCK_STREAM
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import pickle

class ServerSocket(object):
    def __init__(self):
        self.server = socket(AF_INET,SOCK_STREAM)
        self.client = None
    
    def connection_client(self, host='localhost'):
        self.server.bind((host,DEFAULT_TCP_LOGGING_PORT))
        self.server.listen(1)
        new_client, addr = self.server.accept()
        self.client = new_client
        
        #uri = server.recv(1024).decode()
        #self.network = Pyro4.Proxy(uri)
        #server.close()
        
    def run_server(self):
        return self.recv()
    
    def recv(self):
        try:
            return pickle.dumps(self.client.recv(1024))
        except socket.error:
            self.client.close()
            return None
