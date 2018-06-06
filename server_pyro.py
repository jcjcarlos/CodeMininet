#!/usr/bin/env python
from mininet.topo import Topo, SingleSwitchTopo, MinimalTopo
from mininet.topo import SingleSwitchReversedTopo, LinearTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM
import Pyro4
from os import system
Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'json'

class Network (object):
    
    def __init__(self,topo):
        setLogLevel('info')
        self.net = Mininet(topo)
        self.net.start()
        self.elements = {}
        
    def command(self,command):
        if self.get_parameters(command)
            parameters = self.get_parameters(command)
            print ('Argumento valido ' + parameters)
        else:
            print (self.get_parameters(command))
        try:
            self.elements[parameters] = getattr(self.net,command)
        except Exception:
            return ('Valor invalido')
    
    def get_parameters(self,command):
        try:
            parameters = command.split('(')[1].split(')')[0].split(',') 
            return parameters if parameters else None
        except TypeError,Exception:
            pass
    
    def stop(self):
        self.net.stop()

if __name__=='__main__':
    
    setLogLevel('info')
    network = Network(MinimalTopo())
    #daemon = Pyro4.Daemon()
    #topo = MinimalTopo()
    #net = Mininet(topo = topo)
    #net.start()
    #uri = daemon.register(net)
    server = socket(AF_INET,SOCK_STREAM)
    server.bind(('',9876))
    server.listen(1)
    print('*** Wait Client...')
    client,addr = server.accept()
    print('*** Client connected:',addr)
    client.send('Conection estabilished'.encode())
    options = client.recv(1024).decode()
    while options != 'exit':
        client.sendnetwork.command(options)
        options = client.recv(1024).decode()
    #daemon.requestLoop()

            
            
