import socket
import random
import time
from termcolor import colored

class ClienteSensor:
    def __init__(self):
        self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, endereco, porta):
        self.soquete.connect((endereco, porta))

    def gerador_topico(self):
        topicos = ['Luminosidade', 'Irrigacao', 'Trafego']
        topico = random.choice(topicos)
        return topico.upper()

    def gerarValor(self):
        num_aleatorio = random.randint(0, 100)
        return str(num_aleatorio)

    def enviar_mensagem(self, mensagem):
        self.soquete.send(mensagem.encode())
        #pickle.dump(mensagem, self.saida)

    def receber_mensagem(self):
        try:
            mensagem = self.soquete.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def finalizar(self):
        self.soquete.close()

def main():
    while True:
        cliente = ClienteSensor()
        time.sleep(5)
        cliente.connect('localhost', 2222)
        topico = cliente.gerador_topico()
        cliente.enviar_mensagem(f'PUBLICAR, {topico}, {cliente.gerarValor()}')
        resposta = cliente.receber_mensagem()
        print(colored(f'Mensagem do Servidor: {resposta}', "green"))
        cliente.finalizar()

if __name__ == '__main__':
    main()