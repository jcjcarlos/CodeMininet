#!/usr/bin/env python
# -*- coding:utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from os import system

client = socket(AF_INET,SOCK_STREAM)
client.connect(('10.0.0.1',4321))
client.send('Enviando requisicao ao servidor')
print 'Resposta recebida: ' + client.recv(1024)
system('ps -aux | grep xterm')
raw_input('Presione Enter para sair')
