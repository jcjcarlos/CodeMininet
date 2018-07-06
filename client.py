#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
from socket import socket,AF_INET,SOCK_STREAM,error as socket.error
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
#import SocketServer
import ServerSocket
import threading
logging.basicConfig(level=logging.DEBUG,format= '%(levelname)s - %(message)s')

"""
Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'json'
"""

"""           
class StreamRequestMininet(SocketServer.StreamRequestHandler):
    def handle(self):
        logger = self.connection.recv(1024)
        msg = logger.decode('ascii')
        print msg
"""

class ClientNetwork(threading.Thread):
    
    _shutdown = False
    
    def __init__(self):
        super(ClientNetwork,self).__init__()
        self.sock = socket(AF_INET, SOCK_STREAM)
    
    def connect_server(self,host='localhost'):
        logging.debug('Validando IP')
        isValid = self.validate_ip(host)
        logging.debug('O ip é ' + str(isValid))
        tentative = 5
        if isValid:
            try:
                self.sock.connect((host,DEFAULT_TCP_LOGGING_PORT))
                logging.debug('Socket Conectado:' + self.sock.getpeername())
                isValid = True
            except socket.error:
                logging.debug('Error na conexao!')
                pass
        return isValid
    
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
        option = ''
        while not ClientNetwork._shutdown or not option == 'exit':
            option = raw_input('> ')
            self.sock.send(option.encode('ascii'))
              
if __name__ == '__main__':
    client_network = ClientNetwork()
    logging.debug('Conectando ao servidor')
    client_network.connect_server()
    client_network.start()
    
    server_network = ServerSocket.ServerSocket()
    server_network.connection_client()
    server_network.server_forever()
