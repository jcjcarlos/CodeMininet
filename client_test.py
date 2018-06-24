#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
import logging
from logging.handlers import DEFAULT_TCP_LOGGING_PORT
import cPickle as cP
import struct

server = socket(AF_INET,SOCK_STREAM)
server.bind(('',DEFAULT_TCP_LOGGING_PORT))
server.listen(1)
print ('Esperando cliente')
logging.basicConfig(format='%(levelname)s - %(message)s')
client, addr = server.accept()
while True:
    obj = client.recv(4)
    if len(obj) < 4:
        continue
    else:
        tam = struct.unpack('>L', obj)[0]
    log = client.recv(tam)
    record = logging.makeLogRecord(cP.loads(log))
    main_logger = logging.getLogger(record.name)
    main_logger.handle(record)
