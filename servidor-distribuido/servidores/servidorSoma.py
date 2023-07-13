import socket

from termcolor import colored


class OperadorSoma:
    def __init__(self, porta):
        self.soquete_operador_soma = socket.socket()
        self.soquete_operador_soma.bind(('localhost', porta))
        self.soquete_operador_soma.listen(5)

    def finalizar(self):
        self.soquete_operador_soma.close()

    def enviar_mensagem(self, mensagem, soquete_servidor):
        soquete_servidor.send(mensagem.encode())

    def receber_mensagem(self, soquete_cliente):
        try:
            mensagem = soquete_cliente.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def finalizar_conexao(self, cliente_soma):
        cliente_soma.close()

    def calcular_soma(self, mensagem):
        partes = mensagem.split(', ')
        if len(partes) == 3:
            comando, valor1, valor2 = partes
            soma = int(valor1) + int(valor2)
            return str(soma)
        return ''

    def iniciar_operacao(self, servidorDistribuido):
        mensagem = self.receber_mensagem(servidorDistribuido)
        print(colored(f'===============================================================================', 'yellow'))
        print(colored(f'Mensagem recebida do servidor: {mensagem}', 'cyan'))
        soma = self.calcular_soma(mensagem)
        print(colored(f'Resultado da soma: {soma}', 'magenta'))
        print(colored(f'===============================================================================', 'yellow'))
        self.enviar_mensagem(soma, servidorDistribuido)
        self.finalizar_conexao(servidorDistribuido)

def main():
    servidor = OperadorSoma(9090)
    print(colored('Servidor Soma iniciado', 'green'))
    print(colored('Aguardando conexao...', 'green'))
    while True:
        try:
            servidorDistribuido, endereco_servidor = servidor.soquete_operador_soma.accept()
            servidor.iniciar_operacao(servidorDistribuido)
        except KeyboardInterrupt:
            servidor.finalizar()

if __name__ == '__main__':
    main()