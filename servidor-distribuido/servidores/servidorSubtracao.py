import socket
from termcolor import colored

class OperadorSub:
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

    def calcular_sub(self, mensagem):
        partes = mensagem.split(', ')
        if len(partes) == 3:
            comando, valor1, valor2 = partes
            soma = int(valor1) - int(valor2)
            return str(soma)
        return ''

    def iniciar_operacao(self, servidorDistribuido):
        mensagem = self.receber_mensagem(servidorDistribuido)
        print(colored(f'===============================================================================', 'yellow'))
        print(colored(f'Mensagem recebida do servidor: {mensagem}', 'cyan'))
        sub = self.calcular_sub(mensagem)
        print(colored(f'Resultado da subtracao: {sub}', 'magenta'))
        print(colored(f'===============================================================================', 'yellow'))
        self.enviar_mensagem(sub, servidorDistribuido)
        self.finalizar_conexao(servidorDistribuido)

def main():
    servidor = OperadorSub(9191)
    print(colored('Servidor Subtracao iniciado', 'green'))
    print(colored('Aguardando conexao...', 'green'))
    while True:
        try:
            servidorDistribuido, endereco_servidor = servidor.soquete_operador_soma.accept()
            print(colored(f"Conexao aceita de: {endereco_servidor}", 'cyan'))
            servidor.iniciar_operacao(servidorDistribuido)
        except KeyboardInterrupt:
            servidor.finalizar()

if __name__ == '__main__':
    main()