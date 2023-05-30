import optparse

from botnet import Botnet

if __name__ == '__main__':
    botnet = Botnet()
    analisador = optparse.OptionParser('use %prog ' + \
                                       '-H <host alvo> -u <usuario> -F <arquivo senhas>')
    analisador.add_option('-H', dest='host', type='string', \
                          help='espqcifique o host alvo')
    analisador.add_option('-F', dest='arq_senhas', type='string', \
                          help='especifique o arquivo de senhas')
    analisador.add_option('-u', dest='usuario', type='string', \
                          help='especifique o nome do usuario')

    (opcoes, args) = analisador.parse_args()
    file_hosts = opcoes.host
    file_passwords = opcoes.arq_senhas
    file_users = opcoes.usuario

    if file_hosts == None or file_passwords == None or file_users == None:
        print(analisador.usage)
        exit(0)

    botnet.start(file_hosts, file_users, file_passwords)
