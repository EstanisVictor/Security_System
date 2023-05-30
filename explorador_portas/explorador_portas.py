#!/usr/bin/python
# -*- coding: utf-8 -*-
import optparse
from socket import *
from threading import *
import time

def conexaoScan(host, porta):
    try:
        soquete = socket(AF_INET, SOCK_STREAM)
        soquete.connect((host, porta))
        soquete.send('Segurança da Informação\r\n')
        resultados = soquete.recv(100)
        print ('[+] %d/tcp aberta' % porta)
        print(resultados)
    except:
        print ('[-] %d/tcp fechada' % porta)
    finally:
        soquete.close()	

def portaScan(host, portas):
    try:
        IPSite = gethostbyname(host)
    except:
        print ("[-] Nao conseguiu resolver o host '%s'" % host)
        return

    try:
        nomeSite = gethostbyaddr(IPSite)
        print ('\n[+] Resultados para: ' + nomeSite[0])
    except:
        print ('\n[+] Resultados para: ' + IPSite)

    setdefaulttimeout(1)
    for porta in range(1,60000):
        t = Thread(target=conexaoScan,args=(host,int(porta)))
        t.start()
        #time.sleep(0.01)

def inicio():
    analisador = optparse.OptionParser('use explorador_portas '+\
      '-H <host alvo> -p <porta(s) alvo>')
    analisador.add_option('-H', dest='host', type='string',\
      help='especifique o host alvo')
    analisador.add_option('-p', dest='porta', type='string',\
      help='especifique a porta[s] alvo separadas por virgula')

    (opcoes, args) = analisador.parse_args()

    host = opcoes.host
    porta = str(opcoes.porta).split(',')

    if (host == None) | (porta[0] == None):
        print (analisador.usage)
        exit(0)

    portaScan(host, porta)


if __name__ == '__main__':
    inicio()