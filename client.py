#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import SocketServer
import threading

"""
Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'json'
"""

           
class RemoteNetwork(object):
    def __init__(self):
        self.server = socket(AF_INET,SOCK_STREAM)
        self.client = None
    
    def connection_client(self, host='localhost'):
        isValid = self.validate_ip(host):
        if isValid:
            self.server.bind(host,DEFAULT_TCP_LOGGING_PORT)
            self.server.listen(1)
            new_client, addr = self.server.accept()
            self.client = new_client
        
        return isValid
        #uri = server.recv(1024).decode()
        #self.network = Pyro4.Proxy(uri)
        #server.close()
    
    
    
    def send(self,command):
        self.client.send(command.encode('ascii'))
        
    def recv(self):
        return self.client.recv(1024).decode('ascii')


class StreamRequestMininet(SocketServer.StreamRequestHandler):
    def handle(self):
        logger = self.connection.recv(1024)
        msg = logger.decode('ascii')
        print msg

class ClientMininet(threading.Thread):
    
    _shutdown = False
    
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
    
    def connect_server(self,host):
        isValid = self.validate_ip(host)
        if isValid:
            try:
                self.sock.connect((host,DEFAULT_TCP_LOGGING_PORT))
                isValid = True
            except socket.error:
                pass
        return valid
    
    def validate_ip(self,host):
        valid = False
        if isinstance(host,str):
            if not host or host == 'localhost':
                valid = True
            else:
                try:
                    valid = bool(socket.inet_aton(host))
                except socket.error:
                    pass
        return valid
    
    def run(self):
        self.
            
        
        
if __name__ == '__main__':
    network = RemoteNetwork()
    print('Iniciando Conexao')
    network.initialize()
    print('Conexao estabelecida')
    options = ''
    
    options = raw_input('> ')
    network.send(options)
    print network.recv()
    
    network.server.close()
    print('Fim da aplicacao')
    
    
