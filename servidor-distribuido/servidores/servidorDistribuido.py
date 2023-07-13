import socket
from termcolor import colored
from trataServidorCliente import TrataServidorCliente


class Servidor:
    def __init__(self, porta):
        self.soquete_servidor = socket.socket()
        self.soquete_servidor.bind(('localhost', porta))
        self.soquete_servidor.listen(5)

    def enviar_mensagem_cliente(self, mensagem, soquete_cliente):
        soquete_cliente.send(mensagem.encode())

    def receber_mensagem_cliente(self, soquete_cliente):
        try:
            mensagem = soquete_cliente.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def finalizar(self):
        self.soquete_servidor.close()

def main():
    servidor = Servidor(2222)
    print(colored('Servidor Distribuido iniciado', 'green'))
    print(colored('Aguardando conexao...', 'green'))
    while True:
        try:
            cliente, endereco_cliente = servidor.soquete_servidor.accept()
            print(colored(f'===============================================================================', 'yellow'))
            print(colored(f"Conexao aceita de: {endereco_cliente}", 'cyan'))
            mensagem = servidor.receber_mensagem_cliente(cliente)
            trata_cliente = TrataServidorCliente(cliente)
            print(colored(f'Mensagem recebida do cliente: {mensagem}', 'cyan'))
            print(colored(f'===============================================================================', 'yellow'))
            resposta = trata_cliente.iniciar(mensagem)
            servidor.enviar_mensagem_cliente(resposta, cliente)
        except KeyboardInterrupt:
            servidor.finalizar()

if __name__ == '__main__':
    main()