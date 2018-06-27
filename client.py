#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import Topo, SingleSwitchTopo, MinimalTopo
from mininet.topo import SingleSwitchReversedTopo, LinearTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM
import Pyro4
from os import system
from sys import exit
"""
Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'json'
"""

           
class RemoteNetwork(object):
    def __init__(self):
        self.hosts = {}
        self.switches = {}
        self.controllers = {}
        self.network = None
        self.server = socket(AF_INET,SOCK_STREAM)
        self.server.connect(('',9876))
        #uri = server.recv(1024).decode()
        #self.network = Pyro4.Proxy(uri)
        #server.close()
        
    def action(self,command):
        self.server.send(command.encode('ascii'))
        return self.server.recv(1024).decode('ascii')
        
if __name__ == '__main__':
    network = RemoteNetwork()
    print('Iniciando Conexao')
    network.initialize()
    print('Conexao estabelecida')
    options = ''
    
    while options != 'exit':
        options = raw_input('> ')
        print(network.action(options))
    network.server.close()
    print('Fim da aplicacao')
    
    
