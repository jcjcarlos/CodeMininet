# -*- coding: utf-8 -*-
from mininet.log import lg,setLogLevel
import cPickle
import logging

class SocketHandlerMininet(logging.SocketHandler):
    """
    Remocao da quebra de linha dupla na serializacao da mensagem,
    O metodo makePickle foi redefinido para enviar somente a string
    do LogRecord
    """
    
    def makePickle(self, record):
        try:
            msg = record.getMessage() # Ou format(record)
            fmt = '%s'
            sock.send(cPickle.dumps(fmt % msg)) # Codificacao unicode no topo
            return cPickle.dumps(msg)
        except Exception:
            self.handleError( record )
            return cPickle.dumps('*** Error ')

def main():
    socket_handler = SocketHandlerMininet('', DEFAULT_TCP_LOGGING_PORT)
    socket_handler.setLevel(logging.INFO)
    lg.addHandler(socket_handler)
    setLogLevel('info')

if not __name__ == '__main__':
    main()

        
