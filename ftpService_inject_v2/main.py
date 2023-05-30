import optparse
from ftpInject import FTPInject

def inicio():
    analisador = optparse.OptionParser('use main '+\
      '-H <host alvo> -f <arquivo_senhas> -r <texto_redirecionamento>')
    analisador.add_option('-H', dest='host', type='string',\
      help='especifique o host alvo')
    analisador.add_option('-f', dest='arquivo', type='string',\
      help='especifique o arquivo de usuarios e senhas')
    analisador.add_option('-r', dest='redirecionar', type='string',\
      help='especifique o redirecionamento')

    (opcoes, args) = analisador.parse_args()

    host = opcoes.host
    arquivo = opcoes.arquivo
    redirecionar = opcoes.redirecionar

    if (host == None) | (arquivo == None) | (redirecionar == None):
        print (analisador.usage)
        exit(0)

    ftp = FTPInject(host)
    ftp.start(arquivo, redirecionar)

if __name__ == '__main__':
    inicio()