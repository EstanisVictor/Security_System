import termcolor
import requests
import markdown
from bs4 import BeautifulSoup

def get_github_content(url):
    response = requests.get(url)
    
    if response.raise_for_status():
        print(termcolor.colored('Erro ao obter conteúdo do GitHub', 'red'))
    
    content = response.text
    
    return content

def get_phrase_in_github_content(contendReadme):
    soup = BeautifulSoup(contendReadme, 'html.parser')
    
    phrases = []
    
    for tag_pre in soup.find_all('pre'):
        phrases.extend(tag_pre.get_text().split('\n'))

    return phrases

def main():
    
    radmeContent = get_github_content('https://github.com/PyMarcus/daemonium/blob/main/README.md')
    
    mensagemCriptografada = get_phrase_in_github_content(radmeContent)[-1]
    
    alfabeto = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for quantPuloLetra in range(len(alfabeto)):
        mensagemVerdadeira = ''
        for letra in mensagemCriptografada:
            if letra in alfabeto:
                numLetraAlfa = alfabeto.find(letra)
                numLetraAlfa = numLetraAlfa - quantPuloLetra
                if numLetraAlfa < 0:
                    numLetraAlfa = numLetraAlfa + len(alfabeto)
                mensagemVerdadeira = mensagemVerdadeira + alfabeto[numLetraAlfa]
            else:
                mensagemVerdadeira = mensagemVerdadeira + letra
        print(termcolor.colored(f'Pulo #{quantPuloLetra}: {mensagemVerdadeira}', 'cyan'))
        
if __name__ == '__main__':
    main()