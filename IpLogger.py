import socket
import threading
import geocoder
import json
import os

class Logger_link(threading.Thread):
    def __init__(self, url: str, port: int, host_ip: str) -> None:
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", port))
        self.counter = 0
        self.url = url
        self.port = port
        self.host_ip = host_ip
    
    def run(self) -> None:
        print(f"http://{self.host_ip}:{self.port}/")
        while True:
            self.socket.listen(10)
            client, (ip, port) = self.socket.accept()
            threading.Thread(target=self.redirection, args=[client, ip , port]).start()
    
    def redirection(self, client: socket.socket, ip: str, port: int) -> None:
        data = client.recv(4096)
        client.send(f"HTTP/1.1 302 Found\r\nLocation: {self.url}\r\n\r\n".encode())
        client.close()
        info = {
            "localisation": f"{geocoder.ip(socket.gethostbyname(ip)).city}[{geocoder.ip(socket.gethostbyname(ip)).country}]",
            "request": data.decode("utf-8"),
            "request-size": len(data),
        }
        if not os.path.exists("ip"):
            os.mkdir("ip")
        with open(f"ip/{ip}.json", "a+") as file:
            json.dump(info, file, indent=2)

class BDD():
    def __init__(self) -> None:
        try: ...
        except: ...