import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from termcolor import colored

def connect_ifmg(user, pwd):
    try:
        driver = webdriver.Firefox()

        driver.get("https://meu.ifmg.edu.br/Corpore.Net/Login.aspx")

        driver.find_element("id", "txtUser").send_keys(user)

        driver.find_element("id", "txtPass").send_keys(pwd)

        driver.find_element("id", "btnLogin").click()

        if driver.find_element("id", "lbCallUs").text == 'Fale Conosco':
            return True

        return False
    except Exception as e:
        print(colored(e, 'red'))
        return False


def main():
    caminho = '~/Downloads/'
    resultado = 'resultado.txt'
    caminho_expandido = os.path.expanduser(caminho)
    arquivos = os.listdir(caminho_expandido)

    informacoes_validas = []
    for arquivo in arquivos:
        arquivo_completo = os.path.join(caminho_expandido, arquivo)
        if arquivo.startswith('login'):
            print(colored("Testando: "+arquivo_completo, 'magenta'))
            with open(arquivo_completo, 'r') as f:
                content = f.read()
                ra = re.findall(r'RA:\s*(\d+)', content)[0]
                senha = re.findall(r'Senha:\s*([^\n\r]+)', content)[0]
                print(colored(f"RA: {ra} | Senha: {senha.strip()}", 'cyan'))
                if connect_ifmg(ra, senha.strip()):
                    time.sleep(5)
                    informacoes_validas.append(
                        f'RA: {ra}\nSenha: {senha}')
                    print(colored('Conectado com sucesso!', 'green'))
                else:
                    print(colored('Falha na conexão!', 'red'))

    with open(resultado, 'w') as f:
        f.write('\n'.join(informacoes_validas))


if __name__ == '__main__':
    main()
