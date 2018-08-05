#!/usr/bin/env python
# -*- coding:utf-8 -*-

from mininet.topo import Topo, SingleSwitchTopo, MinimalTopo
from mininet.topo import SingleSwitchReversedTopo, LinearTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM, SOL_SOCKET,SO_REUSEADDR
import Pyro4
Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'pickle'

class Network (object):
    def __init__(self,topo):
        self.net = Mininet(topo)
        self.net.start()
    def stop(self):
        self.net.stop()

if __name__=='__main__':
    
    #setLogLevel('info')
    register = Pyro4.Daemon()
    topo = MinimalTopo()
    net = Mininet(topo = topo)
    uri = register.register(net)
    server = socket(AF_INET,SOCK_STREAM)
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    server.bind(('',9876))
    server.listen(1)
    print('Wait Client')
    client,addr = server.accept()
    client.send(str(uri).encode())
    net.start()
    client.close()
    print('Client:',addr)
    register.requestLoop()
            
        
