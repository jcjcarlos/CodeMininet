from mininet.net import Mininet
from mininet.topo import MinimalTopo
from mininet.log import lg,setLogLevel
import logging
from logging.handlers import SocketHandler,DEFAULT_TCP_LOGGING_PORT
from mininet.cli import CLI

if __name__ ==  '__main__':

    socket_handler = SocketHandler('',DEFAULT_TCP_LOGGING_PORT)
    socket_handler.setLevel(logging.INFO)
    socket_handler.setFormatter(logging.Formatter('Socket - %(message)s'))
    lg.addHandler(socket_handler)
    setLogLevel('info')
    network = Mininet(MinimalTopo())
    network.start()
    network.pingAll()
    CLI(network)
    network.stop()
