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

class Network (object):
    def __init__(self,topo):
        self.net = Mininet(topo)
        self.net.start()
        self.except_functions = ['addHost','addSwitch','addController','addNAT']
        self.elements = {}   
        
    def command(self,command):
        if self.get_parameters(command):
            components = self.get_parameters(command)
            print components
            try:
                if not components[0] in self.except_functions:
                    for index in range(len(components[1])):
                        if self.elements.has_key(components[1][index]):
                            components[1][index] = self.elements[components[1][index]]
                    
             
                value = getattr(self.net,components[0])(*components[1])
                if components[0] in self.except_functions:
                    self.elements[components[1][0]] = value
                logging.debug(str(value))
                RemoteLogger.lg.info(str(value))
                print self.elements
                return str(value)
            except Exception,TypeError:
                #logging.debug(str(components))
                logging.debug('Comando nao encontrado')
                return str(None)
        else:
            try:
                return str(getattr(self.net,command)())
            except:
                print ('Argumento invalido')
                return str(None)
    #addLink(get(h1),get(h2))
    
    def get_parameters(self,command):
        try:
            function = command.split('(')[0]
            if len(command.split('(')) >= 2:
                parameters = command.split('(')[1].split(')')[0].split(',')
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
        options = self.server.run_server()
        while options:
            if options == 'exit':
                self.network.stop()
                self.server.close()
                break
            else:
                self.network.command(options)
            options = self.server.run_server()
            
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
    
