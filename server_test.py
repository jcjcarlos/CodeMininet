#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
import logging
from logging.handlers import SocketHandler
"""
server = socket(AF_INET,SOCK_STREAM)
server.bind(('',4321))
server.listen(1)
print 'Esperando cliente'
client, addr = server.accept()
print pickle.loads(client.recv(1024))
"""

server = SocketHandler('',4321)
stringForm = logging.Formatter('%(levelname)s - %(message)s')
server.setFormatter(stringForm)
server.setLevel(logging.INFO)
controller = logging.getLogger(__name__)
controller.setLevel(logging.INFO)
controller.addHandler(server)
controller.info('Teste')



