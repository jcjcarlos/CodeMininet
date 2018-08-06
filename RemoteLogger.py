# -*- coding: utf-8 -*-
from mininet.log import lg,setLogLevel
import pickle
import logging
from logging import handlers
logging.basicConfig(level=logging.DEBUG)

#A biblioteca SocketHandler utiliza cPickle ao inves de pickle
class SocketHandlerMininet(handlers.SocketHandler):
    def __init__(self,host='localhost',port=handlers.DEFAULT_TCP_LOGGING_PORT):
        handlers.SocketHandler.__init__(self,host,port)
        
    """
    Remocao da quebra de linha dupla na serializacao da mensagem,
    O metodo makePickle foi redefinido para enviar somente a string
    do LogRecord
    O método é internamente chamado pela classe SocketHandler para 
    escrita do objeto serializável, durante a execução da método
    handler da super classe
    """
    
    def makePickle(self, record):
        try:
            msg = record.getMessage() # Ou format(record)
            fmt = '%s'
            return pickle.dumps(fmt % msg)
        except:
            self.handleError( record )
            return pickle.dumps('*** Error ')
    

"""
A classe Lg é herdado de Logger, atuando como controlador, permitindo a alteração por ser singleton
"""
setLogLevel('info') #Seta o setLevel do controlador

def connection_addr(addr_client = 'localhost'):
    socket_handler = SocketHandlerMininet(addr_client, handlers.DEFAULT_TCP_LOGGING_PORT)
    socket_handler.setLevel(logging.INFO)
    lg.addHandler(socket_handler)

        
