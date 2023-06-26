import json
import os
import random
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
from collections import defaultdict
from termcolor import colored
import subprocess
import sys

class FibonacciRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.status = 200
        self.ip_requests = defaultdict(int)
        self.blocked_ips = set()

        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            ip_address = self.client_address[0]
            if ip_address in self.blocked_ips:
                self._send_response(403)
                return

            if self.path == "/":
                self._handle_home()
            elif self.path.startswith("/fib"):
                self._handle_fib(self.path.split("/")[2])
            else:
                self._send_response(404)
        except Exception:
            self._send_response(500)
        finally:
            sleep(0.1)

    def log_message(self, format, *args):
        color = "red" if self.status >= 400 else "green"
        host = self.headers.get("Host", "localhost")
        print(
            f'{colored(self.command, color, attrs=["bold"])}/'
            f'{colored(self.status, color, attrs=["bold"])} => '
            f'{colored(f"http://{host}{self.path}", "white")}'
        )

    def _send_response(self, status: int, content_type: str = "application/json"):
        self.status = status
        if status >= 400:
            return self.send_error(status)

        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def _handle_home(self):
        html = os.path.join(self.root_dir, "public", "index.html")
        self._send_response(200, "text/html")

        with open(html, "r") as file:
            html_content = file.read()
        self.wfile.write(html_content.encode())
    def generate_port(self):
        new_port = random.randint(1, 6555)
        while new_port == 8000:
            new_port = random.randint(1, 6555)
        return new_port
    def _handle_fib(self, number_str: str):
        ip_client = self.client_address[0]
        self._load_ip_requests()

        if ip_client not in self.ip_requests:
            self.ip_requests[ip_client] = 1
        elif self.ip_requests[ip_client] < 11:
            self.ip_requests[ip_client] += 1
        else:
            self._block_ip(ip_client)
            self._save_blocked_ips()
            new_port = self.generate_port()
            print(colored("\nServer stopped", "yellow"))
            print(colored(f"\nBlocked IP: {ip_client}", "red"))
            print(colored(f"Restarting server on port: {new_port}", "yellow"))

            python_executable = sys.executable
            script_path = os.path.abspath(__file__)
            subprocess.Popen([python_executable, script_path, str(new_port)], close_fds=True)

            self.server.shutdown()
            self.server.server_close()

            sys.exit()

        self._save_ip_requests()

        start = datetime.now()
        try:
            number = int(number_str)
        except ValueError:
            return self._send_response(400)

        fib = self._calculate_fibonacci(number)
        elapsed_time = datetime.now() - start
        response = {
            "number": number,
            "fib": fib,
            "time": elapsed_time.total_seconds() * 1000,
        }

        self._send_response(200)
        self.wfile.write(json.dumps(response).encode())

    def _calculate_fibonacci(self, n: int):
        x, y = 0, 1
        for _ in range(n):
            x, y = y, x + y
        return x

    def _save_blocked_ips(self):
        with open("blocked_ips.txt", "w") as file:
            file.write("\n".join(self.blocked_ips))

    def _block_ip(self, ip_address):
        self.blocked_ips.add(ip_address)
    def _load_blocked_ips(self):
        if not os.path.isfile("blocked_ips.txt"):
            return

        with open("blocked_ips.txt", "r") as file:
            self.blocked_ips = set(file.read().splitlines())

    def _load_ip_requests(self):
        if not os.path.isfile("ip_requests.txt"):
            return
        with open("ip_requests.txt", "r") as file:
            self.ip_requests = defaultdict(int, json.load(file))

    def _save_ip_requests(self):
        with open("ip_requests.txt", "w") as file:
            json.dump(dict(self.ip_requests), file)
class FibonacciServer:
    def __init__(self, host="localhost", port=8000):
        self.server: HTTPServer = None
        self.host = host
        self.port = port

    def start(self):
        print(colored(f"Server started at http://{self.host}:{self.port}", "yellow"))
        self.server = HTTPServer((self.host, self.port), FibonacciRequestHandler)
        self.server.serve_forever()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print(colored("\nServer stopped", "yellow"))


HOST = "localhost"
PORT = 8000


def run_server(new_port=None):
    try:
        server = FibonacciServer(HOST, new_port or PORT)
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print(colored("Exiting...", "yellow"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        new_port = int(sys.argv[1])
        run_server(new_port)
    else:
        run_server()

# python3 server/main.py