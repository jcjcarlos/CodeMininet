from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI


net = Mininet()

#criando controlador, switchs e hosts
net.addController('c0')
s1 = net.addSwitch('s1')
#s2 = net.addSwitch('s2')
#s3 = net.addSwitch('s3')
h1 = net.addHost('h1')
h2 = net.addHost('h2')
h3 = net.addHost('h3')

#adicionado links
net.addLink(s1,h1)
net.addLink(s1,h2)
net.addLink(s1,h3)
#net.addLink(s1,s2)
#net.addLink(s2,s3)

#Setando comando dos hosts no cmd
if __name__ == '__main__':
	setLogLevel('info')
	net.start()
	net.pingAll()	
	#print(h1.cmd('ping -c1 10.0.0.2 '))
	#print(h1.cmd('python server.py &'))
	#print(h2.cmd('python client.py'))
	CLI(net)
	print 'Encerrando rede...'
	net.stop()
