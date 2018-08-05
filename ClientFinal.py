#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
import pickle
import socket
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import ServerSocket
import threading
from time import sleep
logging.basicConfig(level=logging.DEBUG,format= '%(levelname)s - %(message)s')
ServerSocket.set_name_operator('Client')

"""           
class StreamRequestMininet(ServerSocket.ServerSocket.StreamRequestHandler):
    def handle(self):
        logger = self.connection.recv(1024)
        msg = logger.decode('ascii')
        print msg
"""

class ClientNetwork(threading.Thread):
    """
    Classe que controla o envio de comandos para o servidor. A solicitacao de conexão do cliente inicia a rede virtual no Servidor
    """
    _shutdown = False
    
    def __init__(self):
        super(ClientNetwork,self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    
    def connect_server(self,host='localhost'):
        if self.validate_ip(host):
            try:
                self.sock.connect((host,DEFAULT_TCP_LOGGING_PORT + 1))
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
        logging.debug('start_client')
        option = ''
        while not ClientNetwork._shutdown or not option == 'exit':
            option = raw_input('> ')
            self.sock.send(option.encode())
            
class ServerSocketClient(ServerSocket.ServerSocket,threading.Thread):
    """
    Classe responsável por receber as mensagens do logger do servidor, espera o pedido de conexao do servidor para enviar os registros.
    """
    def __init__(self,port=DEFAULT_TCP_LOGGING_PORT):
        ServerSocket.ServerSocket.__init__(self,port)
        threading.Thread.__init__(self)
        self.cont = 0
    
    def run(self):
        self.accept()
        exit = 0
        while not ClientNetwork._shutdown:
            try:
                recv = self.run_server().decode().rstrip('\n')
                if recv:
                    print recv
                    exit = 0
                else:
                    exit = exit + 1
                if exit == 10:
                    logging.debug('Encerrando Socket')
                    self.close
                    ClientNetwork._shutdown = True
                    break               
                
            except:
                break
if __name__ == '__main__':
    """
    1 - Criar ClientNetwork para enviar comandos para o servidor
    2 - Criar ServerSocketClient para o servidor se conectar ao cliente
    3 - 
    """
    client_network = ClientNetwork()
    if client_network.connect_server():
        server_network = ServerSocketClient(port=DEFAULT_TCP_LOGGING_PORT)
        server_network.start()
        logging.debug('Iniciando envio de comandos')
        client_network.start_client()
      
    else:
        logging.debug('Client não conectou ao server')
