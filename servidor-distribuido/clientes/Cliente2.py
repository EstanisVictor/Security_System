import socket
import random
import time
from termcolor import colored

class Cliente2:
    def __init__(self):
        self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, endereco, porta):
        self.soquete.connect((endereco, porta))

    def escolha_operacao(self):
        operadores = ['SOMA', 'SUBTRACAO']
        operador = random.choice(operadores)
        return operador

    def gerarValor(self):
        num_aleatorio = random.randint(0, 10000000)
        return str(num_aleatorio)

    def enviar_mensagem(self, mensagem):
        self.soquete.send(mensagem.encode())

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
        cliente = Cliente2()
        time.sleep(6)
        cliente.connect('localhost', 2222)
        operacao = cliente.escolha_operacao()
        cliente.enviar_mensagem(f'{operacao}, {cliente.gerarValor()}, {cliente.gerarValor()}')
        resposta = cliente.receber_mensagem()
        print(colored(f'===============================================================================', 'yellow'))
        print(colored(f'Resposta da {operacao}: {resposta}', "cyan"))
        print(colored(f'===============================================================================', 'yellow'))
        cliente.finalizar()

if __name__ == '__main__':
    main()