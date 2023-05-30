
import optparse
import os
from PIL import Image
from bs4 import BeautifulSoup
from termcolor import colored
from PIL.ExifTags import TAGS, GPSTAGS
import urllib3
import exifread
import shutil

http = urllib3.PoolManager()

#https://blogdoenem.com.br/crise-de-29-e-o-nazi-fascismo-historia-enem/
#https://warfarehistorynetwork.com/article/percivals-surrender-britains-greatest-failure/
#https://en.wikipedia.org/wiki/World_War_II
#https://www.defenseone.com/threats/2023/04/the-d-brief-april-27-2023/385697/
#https://www.thecipherbrief.com/the-stakes-in-ukraine-are-greater-than-you-thinkJ
#https://foreignpolicy.com/2023/05/07/lu-shaye-china-wolf-warrior-ambassador-france/
#https://apimagesblog.com/russia-ukraine-war-drafts/2022/7/25/jqy7pt5swa87y0nqk7f3vdw5fnn71n

def createPath(dirName):

    if not os.path.isdir(dirName):
        print(colored(F'[-] O caminho {dirName} não é um diretório', 'red'))
        print(colored(F'[+] Criando o diretório', 'green'))
        os.makedirs(dirName)
        return dirName

    return None

def findImg(url):
    print('[+] Procurando por imagens em: ' + url)
    content = http.request('GET', url)
    soup = BeautifulSoup(content.data, 'html.parser')
    imgTags = soup.findAll('img')
    return imgTags

def downloadImg(imgTag, path):
    try:
        imgSrc = imgTag['src'].split('?')[0]
        print(colored('[+] Baixando imagem: ', 'green'), end='')
        print(colored(imgSrc, 'magenta'))
        imgContent = http.request('GET', imgSrc)
        imgName = imgSrc.split('/')[-1]
        imgFile = open(os.path.join(path, imgName), 'wb')
        imgFile.write(imgContent.data)
        imgFile.close()
        return True
    except Exception as e:
        return None

def exifData(imgName, path):

    print(colored('[+] Extraindo dados de: '+imgName, 'yellow'))

    try:
        with open(os.path.join(path, imgName), 'rb') as imgFile:
            tags = exifread.process_file(imgFile)

            latitude = 'GPS GPSLatitude' in tags
            longitude = 'GPS GPSLongitude' in tags

        if tags:

            # for tag, value in tags.items():
            #     print(colored('    [*] ' + str(tag) +
            #           ' : ' + str(value), 'light_blue'))

            if latitude and longitude:

                lat = tags['GPS GPSLatitude']
                long = tags['GPS GPSLongitude']

                print(colored('    [*] Latitude: ' + str(lat), 'light_green'))
                print(colored('    [*] Longitude: ' +
                      str(long), 'light_green'))
                return True
            else:
                print(
                    colored('    [-] Nenhum dado de localização encontrado', 'red',  'on_white'))
                return False
        else:
            print(colored('    [-] Nenhum dado encontrado', 'red'))
            return False
    except Exception as e:
        print(colored(e, "red"))
        pass


def inicio():
    parser = optparse.OptionParser('use %prog -u <url alvo>')
    parser.add_option('-u', dest='alvo', type='string',
                      help='especifique o alvo')
    (options, args) = parser.parse_args()
    url = options.alvo

    dirName = os.path.join(os.getcwd(), 'downloads')
    path = createPath(dirName)

    if url == None:
        print(parser.usage)
        exit(0)
    else:

        imgTags = findImg(url)

        if path is None:
            path = dirName

        images = []
        for img in imgTags:
            downloadImg(img, path)

        for download in os.listdir(path):
            images.append(download)

        if not images:
            print(colored('[-] Nenhuma imagem encontrada', 'red'))
            exit(0)
        
        print('\n\n')
        
        gps_images = []

        for img in images:
            if img is not None:
                if exifData(img, path):
                    gps_images.append(img)
                else:
                    try:
                        if os.path.isfile(os.path.join(path, img)):
                            os.remove(os.path.join(path, img))
                            print(
                                colored(f"[*] Imagem excluída com sucesso!", 'green', 'on_black'))
                    except Exception as e:
                        print(
                            colored(f"Erro ao excluir {os.path.join(path, img)}: {e}", 'red', 'on_black'))

        gpsFilesDir = os.path.join(os.getcwd(), 'gps_files')

        if not os.path.isdir(gpsFilesDir):
            os.makedirs(gpsFilesDir)

        for img in gps_images:
            shutil.copy(os.path.join(path, img), gpsFilesDir)


if __name__ == '__main__':
    inicio()
