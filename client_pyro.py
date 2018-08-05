#!/usr/bin/env python
# -*- coding:utf-8 -*-
from mininet.topo import Topo, SingleSwitchTopo, MinimalTopo
from mininet.topo import SingleSwitchReversedTopo, LinearTopo
from mininet.net import Mininet
from mininet .log import setLogLevel
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM
import Pyro4

Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'pickle'

class Client:
    
    def __init__(self):
        self.conn_server = socket(AF_INET,SOCK_STREAM)
    
    def initialize():
        pass
        
if __name__ == '__main__':
    setLogLevel('info')
    option = input('Selecione a topologia: ')
    print('Iniciando conexao...')
    conn_server = socket(AF_INET,SOCK_STREAM)
    conn_server.connect(('',9876))
    uri = conn_server.recv(1024).decode()
    print('URI: ' + uri)
    network = Pyro4.Proxy(uri)
    print('Objeto Remoto: ' + str(network))
    network.pingAll()
    network.addHost('h3')
    network.stop()
    #network.iperf()
            
