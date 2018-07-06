# -*- coding: utf-8 -*-
from mininet.log import lg,setLogLevel
import cPickle
import logging
from logging import handlers

#A biblioteca SocketHandler utiliza cPickle ao inves de pickle
class SocketHandlerMininet(handlers.SocketHandler):
    def __init__(self,host='',port=handlers.DEFAULT_TCP_LOGGING_PORT):
        handlers.SocketHandler.__init__(self,host,port)
        
    """
    Remocao da quebra de linha dupla na serializacao da mensagem,
    O metodo makePickle foi redefinido para enviar somente a string
    do LogRecord
    """
    
    def makePickle(self, record):
        try:
            msg = record.getMessage() # Ou format(record)
            fmt = '%s'
            self.sock.send(cPickle.dumps(fmt % msg)) # Codificacao unicode no topo
            return cPickle.dumps(msg)
        except Exception:
            self.handleError( record )
            return cPickle.dumps('*** Error ')

def main():
    socket_handler = SocketHandlerMininet('', handlers.DEFAULT_TCP_LOGGING_PORT)
    socket_handler.setLevel(logging.INFO)
    lg.addHandler(socket_handler)
    setLogLevel('info')

if not __name__ == '__main__':
    main()

        
