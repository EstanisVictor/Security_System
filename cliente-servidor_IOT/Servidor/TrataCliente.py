import json
from termcolor import colored

class TrataCliente:
    def __init__(self, cliente, arquivo_dicionario):
        self.soquete_cliente = cliente
        self.arquivo = arquivo_dicionario
        self.dicionario = {}

    def enviar_mensagem(self, mensagem):
        self.soquete_cliente.send(mensagem.encode())

    def receber_mensagem(self):
        try:
            mensagem = self.soquete_cliente.recv(1024)
            return mensagem.decode()
        except Exception as e:
            print(e)

    def finalizar(self):
        self.soquete_cliente.close()

    def carregar_arquivo(self):
        try:
            with open(self.arquivo, 'r') as f:
                data = f.read()
                return json.loads(data)
        except FileNotFoundError:
            return {}

    def salvar_arquivo(self, dicionario):
        with open(self.arquivo, 'w') as f:
            json_string = json.dumps(dicionario)
            f.write(json_string)
            f.close()

    def iniciar(self):

        mensagem = self.receber_mensagem()

        self.dicionario = self.carregar_arquivo()

        if mensagem.startswith('PUBLICAR'):
            print(colored(f'Mensagem do Cliente Sensor: {mensagem}', 'green'))
            partes = mensagem.split(', ')
            if len(partes) == 3:
                comando, topico, valor = partes
                self.dicionario.update({topico: valor})
                self.salvar_arquivo(self.dicionario)
                self.enviar_mensagem('Topico atualizado com sucesso')
            else:
                self.enviar_mensagem('Erro: Formato inválido para publicar um tópico.')
        elif mensagem.startswith('ASSINAR'):
            print(colored(f'Mensagem do Cliente Atuador: {mensagem}', 'green'))
            partes = mensagem.split(', ')
            if len(partes) == 2:
                comando, topico = partes
                valor = self.dicionario.get(topico, 'Tópico não encontrado')
                self.enviar_mensagem(valor)
            else:
                self.enviar_mensagem('Erro: Formato inválido para consultar um tópico.')
        else:
            self.enviar_mensagem('Comando inválido')

        self.finalizar()