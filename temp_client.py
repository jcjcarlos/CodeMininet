import socket

ip = "127.0.0.1"
porta = 4321

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect((ip,porta))

mensagem = cliente.recv(1024)
print (mensagem.decode('ascii'))
opcao = input('Digite uma opcao')
while (opcao != '-1'):
    cliente.send(opcao.encode('ascii'))
    opcao = raw_input(">")
