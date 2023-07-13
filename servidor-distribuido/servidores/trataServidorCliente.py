import json
import socket
import time


class TrataServidorCliente:
    def __init__(self, cliente):
        self.soquete_cliente = cliente
        self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def enviar_mensagem_operador(self, mensagem):
        self.soquete.send(mensagem.encode())

    def connect_operator(self, endereco, porta):
        self.soquete.connect((endereco, porta))

    def receber_mensagem_operador(self):
        try:
            mensagem = self.soquete.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def finalizar(self):
        self.soquete_cliente.close()

    def iniciar(self, mensagem):
        resposta = ''
        if mensagem.startswith('SOMA'):
            self.connect_operator('localhost', 9090)
            self.enviar_mensagem_operador(mensagem)
            resposta = self.receber_mensagem_operador()
            self.finalizar_conexao_operador()
        elif mensagem.startswith('SUBTRACAO'):
            self.connect_operator('localhost', 9191)
            self.enviar_mensagem_operador(mensagem)
            resposta = self.receber_mensagem_operador()
            self.finalizar_conexao_operador()
        else:
            self.enviar_mensagem_cliente('Comando inválido')

            time.sleep(2)
        return resposta

    def finalizar_conexao_operador(self):
        self.soquete.close()

    def finalizar(self):
        self.soquete_servidor.close()