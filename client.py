#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
import socket
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
#import ServerSocket
from ServerSocket import ServerSocket
import threading
from time import sleep
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
    def connect_server(self,host='localhost'):
        if self.validate_ip(host):
            try:
                self.sock.connect((host,DEFAULT_TCP_LOGGING_PORT + 1))
                logging.debug('Cliente se conectou ao Servidor')
                return True
            except socket.error:
                logging.debug('Error na conexao!')
        return False
    
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
    
    def start_client(self):
        option = ''
        while not ClientNetwork._shutdown or not option == 'exit':
            option = raw_input('> ')
            self.sock.send(option.encode('ascii'))
            
class ServerSocketClient(ServerSocket,threading.Thread):
    def __init__(self,port=DEFAULT_TCP_LOGGING_PORT):
        ServerSocket.__init__(self,port)
    
    def run(self):
        self.server_forever()
              
if __name__ == '__main__':
    client_network = ClientNetwork() #Thread que conecta a um servidor,
    if client_network.connect_server():
        server_network = ServerSocket(port=DEFAULT_TCP_LOGGING_PORT)
        logging.debug('Esperando conexão do servidor')
        server_network.connection_client() #Espera o servidor conectar ao socket, através da classe ServerSocket
        logging.debug('Cliente foi conectado pelo Servidor')
        client_network.start_client()
        server_network.start()
    else:
        logging.debug('Client não conectou ao server')
