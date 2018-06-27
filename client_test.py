#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from SocketServer import StreamRequestHandler, ThreadingTCPServer
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import cPickle as cP
import struct

DEFAULT_HOST = 'localhost'

class SocketServerMininet (ThreadingTCPServer):
    allow_reuse_address = True
    
    def __init__(self, host=DEFAULT_HOST,port = DEFAULT_TCP_LOGGING_PORT):
        ThreadingTCPServer.__init__(self,(host, port),LogRecordMininet)
        
    def run_server(self):
        pass
        
server = socket(AF_INET,SOCK_STREAM)
server.bind(('',4321))
server.listen(1)
print server.fileno()
print ('Esperando cliente')
print server.fileno()
logging.basicConfig(format='%(message)s')
client, addr = server.accept()
msg = ''
while True:
    msg += cP.loads(client.recv(1024))
    print msg
"""
    obj = client.recv(4)
    if len(obj) < 4:
        continue
    else:
        tam = struct.unpack('>L', obj)[0]
    log = client.recv(tam)
    record = logging.makeLogRecord(cP.loads(log))
    main_logger = logging.getLogger(record.name)
    main_logger.handle(record)
"""
