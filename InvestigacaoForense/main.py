import optparse
from PyPDF2 import PdfReader
import subprocess
import os
from termcolor import colored
import time

author_file: str


def directory_contains_pdf_files(path):
    # Verificar se o caminho passado é um diretório
    if not os.path.isdir(path):
        print(colored(F'[-] O caminho {path} não é um diretório', 'red'))
        print(colored(F'[+] Criando o diretório', 'green'))

        time.sleep(2)

        return False

    # Verificar se o diretório contém pelo menos um arquivo PDF
    for filename in os.listdir(path):
        if filename.endswith('.pdf'):
            return True

    # Se nenhum arquivo PDF foi encontrado, retornar False
    return False


def generate_path_download(dir_path):

    # caso não exista o diretório, irá criar
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # lista de urls para download
    url_list = ['http://www.africau.edu/images/default/sample.pdf',
                'http://www.pdf995.com/samples/pdf.pdf',
                'https://www.iso.org/files/live/sites/isoorg/files/store/en/PUB100080.pdf',
                'https://www.nature.com/articles/nature09534.pdf',
                'https://www.tutorialspoint.com/java/java_tutorial.pdf',
                'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
                'https://www.sec.gov/about/offices/ocie/risk-alert-cybersecurity-ransomware-alert.pdf',
                'http://www.escolasapereira.com.br/storage/post_arquivos/634/17307_Mat_1.pdf',
                'https://www.pjf.mg.gov.br/secretarias/sarh/edital/interno/selecao2013/2013/material_de_estudo/matematica/anexos/exercicios.pdf',
                'https://www.c7s.com.br/wp-content/uploads/2019/07/Matem%C3%A1tica-7%C2%B0-ano.pdf'
                ]

    # baixando os arquivos
    for url in url_list:
        runcmd(f"wget -P {dir_path} {url}", verbose=True)


def runcmd(cmd, verbose=False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

    stdout, stderr = process.communicate()
    if verbose:
        print(stdout.strip(), stderr)
    pass


def print_metadata_files(file):
    # lendo e mostrando os metadados do arquivo
    file_pdf = PdfReader(open(file, 'rb'))
    info_metadata = file_pdf.metadata
    print(colored('[*] Metadados para o arquivo: ' +
          os.path.basename(file), "cyan"))
    for item in info_metadata:
        print(colored(f'    [+] ' + item + ':' +
                      info_metadata[item], "magenta"))
        time.sleep(0.1)


def get_author_metadata(file, author_parser: str):
    # pegando o autor do arquivo
    file_pdf = PdfReader(open(file, 'rb'))
    info_metadata = file_pdf.metadata
    author: str = info_metadata.get('/Author', 'Autor não encontrado')

    if author_parser.lower() == author.lower():
        return author

    return False


def main():
    parse = optparse.OptionParser("use: %prog -A <'autor'>")
    parse.add_option('-A', dest='author', type='string',
                     help='especifique o autor do PDF')

    (option, args) = parse.parse_args()
    autor_parser: str = option.author

    # criando o diretório para armazenar os arquivos
    dir_path = os.path.join(os.getcwd(), 'downloads')

    # verificando se é um diretório e se contém arquivos pdf
    if not directory_contains_pdf_files(dir_path):
        # baixando os arquivos pdfs usando wget
        print(colored(F'\n[+] Iniciando Donwload', 'green'))
        time.sleep(2)

        generate_path_download(dir_path)
        print(colored(f'[+] Download dos arquivos PDFs concluído', "green"))
        time.sleep(1)
    else:
        print(
            colored(f'[+] Já existe o dieretorio com os arquivos PDFs', "light_blue"))
        time.sleep(1)

    if autor_parser == None:
        print(colored(f'[-]'+parse.usage, "red"))
        exit(0)
    else:
        # listando os arquivos pdfs
        pdf_files = [f for f in os.listdir(dir_path)]
        # pegando os autores dos arquivos
        for file in pdf_files:
            print_metadata_files(os.path.join(dir_path, file))

        verify = False

        files = []

        for file in pdf_files:
            author_file = get_author_metadata(
                os.path.join(dir_path, file), autor_parser)
            if author_file:
                verify = True
                files.append(file)

        with open('autor_pdf.txt', 'w') as txt:
            txt.write(f'{autor_parser}\n')
            for f in files:
                txt.write(f'  {f}\n')

        if verify:
            print(colored(
                f'[+] O autor {autor_parser} foi encontrado nos arquivos PDFs', "green"))
        else:
            print(colored(
                f'[-] O autor {autor_parser} não foi encontrado nos arquivos PDFs', "red"))


if __name__ == '__main__':
    main()
