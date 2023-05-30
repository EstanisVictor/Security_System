#!/usr/bin/python3
# -*- coding: utf-8 -*-
import zipfile
import optparse
from threading import Thread
import os
from email.message import EmailMessage
import ssl
import smtplib

def sendEmail(senha):
    
    email_sender = '<email@example.com>'
    email_password = '<password email token>'
    email_reciver = '<email@example.com>'
    
    subject = senha
    
    body = """
        Quebra Senha {senha}
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciver, em.as_string())
        

def extrairArquivo(arquivo, senha):
    try:
        arquivo.extractall(pwd=bytes(senha, 'utf-8'))
        print ('[+] Senha encontrada: ' + senha + '\n')
        sendEmail(senha)
    except:
        pass


def inicio():
    analisador = optparse.OptionParser("use %prog "+\
      "-f <arquivozip> -d <dicionario>")
    analisador.add_option('-f', dest='nomezip', type='string',\
      help='especifique o arquivo zip')
    analisador.add_option('-d', dest='nomedic', type='string',\
      help='especifique o arquivo dicionario')
    (opcoes, argumentos) = analisador.parse_args()
    if (opcoes.nomezip == None) | (opcoes.nomedic == None):
        print (analisador.usage)
        exit(0)
    else:
        nomezip = opcoes.nomezip
        nomedic = opcoes.nomedic

    ArquivoZipe = zipfile.ZipFile(nomezip)
    arquivoDici = open(nomedic)

    for linha in arquivoDici.readlines():
        senha = linha.strip('\n')
        t = Thread(target=extrairArquivo, args=(ArquivoZipe, senha))
        t.start()


if __name__ == '__main__':
    inicio()