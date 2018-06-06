#!/usr/bin/env python
from mininet.topo import Topo, SingleSwitchTopo, MinimalTopo
from mininet.topo import SingleSwitchReversedTopo, LinearTopo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from socket import socket,AF_INET,SOCK_STREAM
import Pyro4
from os import system
import pickle
Pyro4.config.SERIALIZERS_ACCEPTED = set(['json', 'marshal', 'serpent','pickle'])
Pyro4.config.SERIALIZER = 'json'

class Network (object):
    def __init__(self,topo):
        setLogLevel('info')
        self.net = Mininet(topo)
        self.net.start()
        self.elements = {}
        
    def command(self,command):
        if self.get_parameters(command):
            elements = self.get_parameters(command)
            print ('Argumento valido ' + str(elements)))
            try:
                self.elements[parameters] = getattr(self.net,command)(parameters)
                print('Reconhecer parametro')
                return str(self.elements[parameters])
            except:
                print ('Valor Invalido')
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
            parameters = command.split('(')[1].split(')')[0].split(',')
            print parameters
            return list(function,parameters)
        except:
            print ('Argumento invalido')
            return None
    
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
        client.send(network.command(options).encode('ascii'))
        options = str(client.recv(1024).decode('ascii'))
    #daemon.requestLoop()
