#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mininet.topo import *
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
import socket
import threading

porta = 9876

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(('',porta))

server.listen(1)

print ("Ouvindo")

while True:
	client,addr = server.accept()
	print ("Conexao recebida ",addr)
	client.send("Ola cliente".encode('ascii'))
	mensagem = client.recv(1024)
	print("Topologia criada: ")
	if (mensagem.decode('ascii') == '1'):
		print("SingleTopo")
		topo = SingleSwitchTopo()
	elif(mensagem.decode('ascii') == '2'):
		print("LinearTopo")
		topo = LinearTopo()
	elif(mensagem.decode('ascii') == '3'):
		print("MinimalTopo")
		topo = MinimalTopo()
	else: 
		print("Invalida")
	if topo:
		setLogLevel('info')
		net = Mininet(topo=topo)
		net.start()
		CLI(net)
		net.stop()		
	client.close()
