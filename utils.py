import socket
import threading
import pycli
from datetime import datetime
import random
import subprocess
import os
import requests
import zipfile
import shutil

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
        print(f"{pycli.pycli.colored("00FF00", "[Online]")} http://{self.host}:{self.port}/")
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
        print(f"{pycli.pycli.colored('[', 'FF0000')}{pycli.pycli.colored(f'{ip}:{port}', "FFFA00")}{pycli.pycli.colored(']', "FF0000")} Send {size} Bytes")

def txt_art():
    return f"""
    {pycli.colored("                .", "FFA500")} 
    {pycli.colored("             .~5P.", "FFA500")}
    {pycli.colored("           :JB&&G:", "FFA500")}
    {pycli.colored("         ^YB&&&#P^", "FFA500")}
    {pycli.colored("       :JGB####B5!", "FFA500")}
    {pycli.colored("     .~5GBBGGGGG5J:", "FFA500")}
    {pycli.colored("    .~5PPPPPP5555J?:", "FFA500")}
    {pycli.colored("    .J555YYYYJJJJJ??!:                  88888888 88                   ", "FFA500")}
    {pycli.colored("    .!5YYJJ???77777!!7!^.               88                            ", "FFA500")}{pycli.colored("88       88", "FF0000")}
    {pycli.colored("   !7:~", "FF0000")}{pycli.colored("JJJ??777!!!~~~~~!!^.             88       88  888888   888888  ", "FFA500")}{pycli.colored("88  888  88  888888   888888   888888", "FF0000")}
    {pycli.colored("  ^PP57", "FF0000")}{pycli.colored("^~7?77!!!~~~^^^~~~!!^            88888    88 88    88 88    88 ", "FFA500")}{pycli.colored("88 88 88 88       88 88    88 88    88", "FF0000")}
    {pycli.colored(" .Y5555Y!:", "FF0000")}{pycli.colored("^!77!~~~^^^^^^~~!!!.          88       88 88       88888888 ", "FFA500")}{pycli.colored("8888   8888  8888888 88       88888888", "FF0000")}
    {pycli.colored(" !5YJJJJJ?~.", "FF0000")}{pycli.colored(".^!!~~^^^^~~~~!!7?:         88       88 88       88       ", "FFA500")}{pycli.colored("888     888 88    88 88       88", "FF0000")}
    {pycli.colored(".JJ???777777: ", "FF0000")}{pycli.colored(".^!!~~~~~~!!!77?7         88       88 88        8888888 ", "FFA500")}{pycli.colored("88       88  8888888 88        8888888", "FF0000")}
    {pycli.colored(":J?77!!!~~~!!~. ", "FF0000")}{pycli.colored(".~7!!!!!7777?J7   ", "FFA500")}
    {pycli.colored(".??7!!~~^^^^~!!. ", "FF0000")}{pycli.colored(".~?77777???J?.", "FFA500")}
    {pycli.colored(" ^?77!~~^^^~~!7^ ", "FF0000")}{pycli.colored(".^?????JJJJ!.", "FFA500")}
    {pycli.colored("  .~777!!!!!!!7! ", "FF0000")}{pycli.colored(".~JJJJYYJ!.", "FFA500")}
    {pycli.colored("    .:!7?7777??~ ", "FF0000")}{pycli.colored(".!YY5YJ~.", "FFA500")}
    {pycli.colored("       .^!?JJJY^ ", "FF0000")}{pycli.colored(".J5J!:", "FFA500")}
    {pycli.colored("          .:!JY. ", "FF0000")}{pycli.colored(".~.", "FFA500")}
    """

def path_format(base_path: str, path: str) -> str:
    if os.path.isdir(path):
        path = os.path.normpath(path)
    elif os.path.isdir(os.path.join(base_path, path)):
        path = os.path.normpath(os.path.join(base_path, path))
    else:
        print("Path not file.")
    return path

def version() -> str:
    return "1.0.0a"

def restart() -> None:
    os.kill(os.getpid(), 9)

def update() -> None:
    do_update = False
    result = subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True)
    if result.stdout:
        do_update = True
        for i in result.stdout.split("\n")[-2:-1]:
            lib = i.split(" ")[0]
            subprocess.run(["pip", "install", "--upgrade", lib])
    response = requests.get(f"https://api.github.com/repos/Overdjoker048/IpTools/releases")
    if response.status_code == 200:
        do_update = True
        release_info = response.json()[0]
        if release_info:
            latest_version = release_info["tag_name"]
            if latest_version != version():
                download_url = release_info["assets"][0]["browser_download_url"]
                response = requests.get(download_url, stream=True)
                with open('update.zip', 'wb') as file:
                    for chunk in response.iter_content(chunk_size=128):
                        file.write(chunk)
                with zipfile.ZipFile('update.zip', 'r') as zip_ref:
                    zip_ref.extractall('temp_update')
                os.remove('update.zip')
                for item in os.listdir('temp_update'):
                    s = os.path.join('temp_update', item)
                    d = os.path.join('.', item)
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.move(s, d)
                    else:
                        shutil.move(s, d)
                shutil.rmtree('temp_update')
    if do_update:
        restart()