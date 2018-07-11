#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
import RemoteLogger
import pickle
from ServerSocket import ServerSocket
from os import system
from time import sleep
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s - %(message)s')
"""
Tentativa com pickle, problemas para serialização das instancias da classe Mininet
Não é possível serializar arquivos

import Pyro4
import pickle
Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'json'
"""

class Network (object):
    def __init__(self,topo):
        self.net = Mininet(topo)
        self.net.start()
        self.elements = {}
    
        
    def command(self,command):
        if self.get_parameters(command):
            components = self.get_parameters(command)
            try:
                value = getattr(self.net,components[0])(*components[1])
                print repr(value)
                print str(value)
                return repr(value)
            except Exception,TypeError:
                return str(None)
        else:
            try:
                return str(getattr(self.net,command)())
            except:
                print ('Commando sem argumento invalido')
                return str(None)
    
    def get_parameters(self,command):
        try:
            function = command.split('(')[0]
            if len(command.split('(')) >= 2:
                parameters = command.split('(')[1].split(')')[0].split(',')
            else:
                parameters = None
            return [function,parameters]
        except:
            print ('Argumento invalido')
            return None
    
    def stop(self):
        self.net.stop()
        
class ControllerNetwork(object):
    def __init__(self):
        self.network = Network(MinimalTopo())
        self.server = ServerSocket(port=DEFAULT_TCP_LOGGING_PORT + 1)#Socket que recebe comandos do cliente
    def initialize(self,host='localhost'):
        return self.server.connection_client()#Aguardando cliente conectar ao servidor
            
    def run(self):
        options = ''
        while not options == 'exit':
            options = pickle.loads(self.server.run_server())
            self.network.command(options)        

if __name__=='__main__':
    logging.debug('Inicializando controlador de rede...')
    controlNetwork = ControllerNetwork()
    logging.debug('Aguardando conexão do cliente...')
    client = controlNetwork.initialize() #chama o método do Server connection_client e espera um cliente conectar
    logging.debug('O Servidor foi conectado pelo cliente')
    if client:
        sleep(1)
        RemoteLogger.connection_addr(client[0]) #connect do Logger, se conecta a um servidor, thread interno
        logging.debug('O Servidor se conectou ao cliente')
    controlNetwork.run()
    """
    1 - Tentavia via Pyro4
    daemon = Pyro4.Daemon()
    topo = MinimalTopo()
    net = Mininet(topo = topo)
    net.start()
    uri = daemon.register(net)
    daemon.requestLoop()
    """
    
    #2 - Tentativa via Socket   
