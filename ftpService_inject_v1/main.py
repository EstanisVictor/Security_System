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
    file = opcoes.arquivo
    content = opcoes.redirecionar

    if (host == None) | (file == None) | (content == None):
        print (analisador.usage)
        exit(0)

    ftp = FTPInject(host)
    ftp.start(file, content)

if __name__ == '__main__':
    inicio()