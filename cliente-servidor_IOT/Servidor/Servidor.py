import socket
import TrataCliente

class Servidor:
    def __init__(self, porta):
        self.soquete_servidor = socket.socket()
        self.soquete_servidor.bind(('localhost', porta))
        self.soquete_servidor.listen(5)
        self.file = 'dictionary.txt'

    def finalizar(self):
        self.soquete_servidor.close()

def main():
    servidor = Servidor(2222)
    while True:
        try:
            cliente, endereco_cliente = servidor.soquete_servidor.accept()
            print("Conexao aceita de: ", endereco_cliente)
            trata_cliente = TrataCliente.TrataCliente(cliente, servidor.file)
            trata_cliente.iniciar()
        except KeyboardInterrupt:
            servidor.finalizar()

if __name__ == '__main__':
    main()