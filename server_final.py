#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
import RemoteLogger
import pickle
import ServerSocket
from os import system
from time import sleep
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s - %(message)s')
ServerSocket.set_name_operator('Server')
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
                logging.debug(str(value))
                return str(value)
            except Exception,TypeError:
                logging.debug(str(components))
                logging.debug('Comando nao encontrado')
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
                print parameters
            else:
                parameters = None
            return [function,parameters]
        except:
            logging.debug('Argumento invalido')
            return 'Argumento invalido'
    
    def stop(self):
        self.net.stop()
        
class ControllerNetwork(object):
    def __init__(self):
        self.server = ServerSocket.ServerSocket(port=DEFAULT_TCP_LOGGING_PORT + 1) #Socket que recebe comandos do cliente
    
    def accept_client(self):
        return self.server.accept()
    
    def initialize(self):
        #Aguardando cliente conectar ao servidor
        self.network = Network(MinimalTopo())
            
    def run(self):
        options = ''
        while not options == 'exit':
            options = self.server.run_server().decode()
            print options
            self.network.command(options)
            
if __name__=='__main__':
    controlNetwork = ControllerNetwork()
    client_addr = controlNetwork.accept_client() #Aguarda cliente se conectar para receber os comandos
    if client_addr:
        logging.debug('Cliente conectado' + str(client_addr))
        RemoteLogger.connection_addr(client_addr[0])
        controlNetwork.initialize()
        controlNetwork.run()
    else:
        logging.debug('Cliente não conectado')
    
    
    #connect do Logger, se conecta a um servidor, thread interno
    controlNetwork.run()
    #logging.debug('O Cliente não se conectou')

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
