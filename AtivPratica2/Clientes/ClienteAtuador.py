import socket
import time
import random
from termcolor import colored

class ClienteAtuador:
    def __init__(self):
        self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self, endereco, porta):
        self.soquete.connect((endereco, porta))

    def gerador_topico(self):
        topicos = ['Luminosidade', 'Irrigacao', 'Trafego']
        topico = random.choice(topicos)
        return topico.upper()

    def enviar_mensagem(self, mensagem):
        self.soquete.send(mensagem.encode())

    def receber_mensagem(self):
        try:
            mensagem = self.soquete.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def verifica_mensagem(self, mensagem):
        if int(mensagem) >= 60:
            print(colored("Abrindo Cortina", 'cyan'))
        else:
            print(colored("Fechando cortina", 'magenta'))

    def finalizar(self):
        self.soquete.close()

def main():
    while True:
        cliente = ClienteAtuador()
        time.sleep(10)
        cliente.connect('localhost', 2222)
        topico = cliente.gerador_topico()
        cliente.enviar_mensagem(f'ASSINAR, {topico}')
        resposta = cliente.receber_mensagem()
        print(colored(f'Mensagem do Servidor: {resposta}', "green"))
        cliente.verifica_mensagem(resposta)
        cliente.finalizar()

if __name__ == '__main__':
    main()