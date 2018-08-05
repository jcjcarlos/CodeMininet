#!/usr/bin/env python
# -*- coding:utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET,SO_REUSEADDR
from os import system

server = socket(AF_INET,SOCK_STREAM)
server.bind(('',4321))
server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
server.listen(1)
print ('Servidor online aguardando requisição...')
client = server.accept()
client[0].send('Requisicao aceita')
print str(client) + ' ' + client[0].recv(1024)
system('ps -aux | grep xterm')
raw_input('Presione Enter para sair')
