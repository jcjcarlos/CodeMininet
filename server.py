#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM
import RemoteLogger
from os import system
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

if __name__=='__main__':
    network = Network(MinimalTopo())
    """
    1 - Tentavia via Pyro4
    daemon = Pyro4.Daemon()
    topo = MinimalTopo()
    net = Mininet(topo = topo)
    net.start()
    uri = daemon.register(net)
    """
    
    #2 - Tentativa via Socket
    server = socket(AF_INET,SOCK_STREAM)
    server.bind(('',9876))
    server.listen(1)
    print('*** Wait Client...')
    client,addr = server.accept()
    print('*** Client connected:',addr)
    client.send('Conection estabilished'.encode())
    options = client.recv(1024).decode()
    while options != 'exit':
        client.send(network.command(options).encode('ascii'))
        options = str(client.recv(1024).decode('ascii'))
    client.close()
    #daemon.requestLoop()