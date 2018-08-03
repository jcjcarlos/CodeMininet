# -*- coding: utf-8 -*-
from mininet.log import lg,setLogLevel
import cPickle
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
            #Evitar erros na serialização de objetos que não sejam do tipo str
            fmt =  '%s'
            return msg.encode()
        except:
            self.handleError( record )
            return cPickle.dumps('*** Error ')
        
    #Metodo para utilizar os socket criado pela classe para enviar e receber comandos
    def send(self,s):
        """
        Metodo redefinido para debugar o envio de mensagems pelo socketHandler
        """
        if self.sock is None:
            self.createSocket()
            
        else:
            try:
                self.sock.sendall(s)
                self.flush()
            except OSError:
                logging.debug('Mensagem' + cPickle.dumps(s) + ' nao enviada')

"""
A classe Lg é herdado de Logger, atuando como controlador, permitindo a alteração por ser singleton
"""
setLogLevel('info') #Seta o setLevel do controlador

def connection_addr(addr_client = 'localhost'):
    socket_handler = SocketHandlerMininet(addr_client, handlers.DEFAULT_TCP_LOGGING_PORT)
    socket_handler.setLevel(logging.INFO)
    lg.addHandler(socket_handler)

def getSocket():
    return lg.handlers[1].getSocket()

        
