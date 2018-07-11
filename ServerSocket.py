#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import socket,AF_INET,SOCK_STREAM,error as socket_exception
from socket import SOL_SOCKET, SO_REUSEADDR
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import pickle
import logging
logging.basicConfig(level=logging.DEBUG)

class ServerSocket(object):
    def __init__(self,port=DEFAULT_TCP_LOGGING_PORT):
        self.server = socket(AF_INET,SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.client = None
        self.port = port
    
    def connection_client(self, host='localhost'):
        self.server.bind((host,self.port))
        self.server.listen(1)
        try:
            new_client, addr = self.server.accept()
            self.client = new_client
            logging.debug('ServerSocket conectado:' + str(addr))
            return addr
        except socket_exception:
            return None
        
        #uri = server.recv(1024).decode()
        #self.network = Pyro4.Proxy(uri)
        #server.close()
        
    def run_server(self):
        return self.recv()
    
    def recv(self):
        try:
            return pickle.dumps(self.client.recv(1024))
        except socket_exception:
            self.client.close()
            return None
