from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI


net = Mininet()

class SingleSwitchTopo( Topo ):
    def build( self, n=2):
        switch = self.addSwitch('s1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1)
            self.addLink(host, switch)
           

#criando controlador, switchs e hosts
c1 = net.addController('c1',port=6633)
c2 = net.addController('c2',port=6634)
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
h1 = net.addHost('h1')
h2 = net.addHost('h2')

#adicionado links
net.addLink(s1,h1)
net.addLink(s2,h2)
net.addLink(s1,s2)

#iniciando controladores de switches
c1.start()
c2.start()
s1.start([c1])
s2.start([c2])

#Setando comando dos hosts no cmd
if __name__ == '__main__':
	setLogLevel('info')
	net.start()
	net.pingAll()	
	CLI(net)
	print 'Encerrando rede...'
	net.stop()
