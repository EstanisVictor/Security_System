from pexpect import pxssh


class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            print("[+] Connected to user <" + self.user + "> using password <" + self.password + ">")
            return s
        except Exception as e:
            print(e)
            print("[-] Error connecting")

    def send_command(self, cmd):
        if self.session:
            self.session.sendline(cmd)
            self.session.prompt()
            return self.session.before