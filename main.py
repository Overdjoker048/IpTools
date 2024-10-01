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

my_ip = ""
scanned_port = 0

def get_ip() -> None:
    global my_ip
    my_ip = requests.get("https://httpbin.org/ip").json()["origin"]

threading.Thread(target=get_ip).start()

prompt_design = colored("\n┌─[", "FF0000")+colored("{}", "FFFFF")+colored("]", "FF0000")+colored("@", "FFA000")+colored("[", "FF0000")+colored("{}")+colored("]", "FF0000")+colored(":~\n", "1A1A1A")+colored("└>", "FF0000")+colored(" $ ", "FFA500")
cli = CLI(prompt=prompt_design, anim=True, logs=True, user=os.getlogin(), title="FireWare")

display = f"""{colored("                .", "FFA500")} 
{colored("             .~5P.", "FFA500")}
{colored("           :JB&&G:", "FFA500")}
{colored("         ^YB&&&#P^", "FFA500")}
{colored("       :JGB####B5!", "FFA500")}
{colored("     .~5GBBGGGGG5J:", "FFA500")}
{colored("    .~5PPPPPP5555J?:", "FFA500")}
{colored("    .J555YYYYJJJJJ??!:                  88888888 88                   ", "FFA500")}
{colored("    .!5YYJJ???77777!!7!^.               88                            ", "FFA500")}{colored("88       88", "FF0000")}
{colored("   !7:~", "FF0000")}{colored("JJJ??777!!!~~~~~!!^.             88       88  888888   888888  ", "FFA500")}{colored("88  888  88  888888   888888   888888", "FF0000")}
{colored("  ^PP57", "FF0000")}{colored("^~7?77!!!~~~^^^~~~!!^            88888    88 88    88 88    88 ", "FFA500")}{colored("88 88 88 88       88 88    88 88    88", "FF0000")}
{colored(" .Y5555Y!:", "FF0000")}{colored("^!77!~~~^^^^^^~~!!!.          88       88 88       88888888 ", "FFA500")}{colored("8888   8888  8888888 88       88888888", "FF0000")}
{colored(" !5YJJJJJ?~.", "FF0000")}{colored(".^!!~~^^^^~~~~!!7?:         88       88 88       88       ", "FFA500")}{colored("888     888 88    88 88       88", "FF0000")}
{colored(".JJ???777777: ", "FF0000")}{colored(".^!!~~~~~~!!!77?7         88       88 88        8888888 ", "FFA500")}{colored("88       88  8888888 88        8888888", "FF0000")}
{colored(":J?77!!!~~~!!~. ", "FF0000")}{colored(".~7!!!!!7777?J7   ", "FFA500")}
{colored(".??7!!~~^^^^~!!. ", "FF0000")}{colored(".~?77777???J?.", "FFA500")}
{colored(" ^?77!~~^^^~~!7^ ", "FF0000")}{colored(".^?????JJJJ!.", "FFA500")}
{colored("  .~777!!!!!!!7! ", "FF0000")}{colored(".~JJJJYYJ!.", "FFA500")}
{colored("    .:!7?7777??~ ", "FF0000")}{colored(".!YY5YJ~.", "FFA500")}
{colored("       .^!?JJJY^ ", "FF0000")}{colored(".J5J!:", "FFA500")}
{colored("          .:!JY. ", "FF0000")}{colored(".~.", "FFA500")}
"""
print(display)

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
    echo(txt)
    scanned_port = 0

@cli.command(alias=["dl"])
def download(ip: str, port: int = 80) -> None:
    "Create an html file from the ip response."
    headers = {"User-Agent": UserAgent().random}
    reponse = requests.request("GET", f"http://{ip}:{port}/", headers=headers)
    if reponse.status_code == 200:
        print(f"{ip}_{port} has been successfully downloaded.")
        print(f"[Path] {os.path.join(CLI.home, 'output', f'{os.path.splitext(ip)[0]}.{port}.html')}")
        if not os.path.exists("output"):
            os.mkdir("output")
        print(os.path.splitext(ip))
        with open(os.path.join("output", f"{os.path.splitext(ip)[0]}.{port}.html"), "wb") as file:
            file.write(reponse.text.encode("utf-8"))
    else:
        print(f"The query returned an error code: {reponse.status_code}")

@cli.command(alias=["ls"])
def dir() -> None:
    "Display all file in directory."
    files = os.listdir(cli.path)
    maxlenght = 0
    for i in files:
        if len(i) > maxlenght:
            maxlenght = len(i)

    echo(f"{'Name'}{(maxlenght-4)*' '} | Last modification   | Perm  | Size")
    echo((39+maxlenght)*"-")
    text = ""
    for i in files:
        file = os.path.join(cli.path, i)
        color = utils.color_file(file)
        data = os.stat(file)
        text += f"{colored(i, color=color)}{(maxlenght-len(i))*' '} | {time.strftime("%S:%M:%H %m:%d:%Y", time.localtime(os.path.getmtime(file)))} | {data.st_mode} | {utils.bytes_convert(data.st_size)}\n"
    echo(text[:-1])

@cli.command(alias=["run"])
def start(path: str) -> None:
    "launch file."
    os.system(os.path.join(cli.path, path))

@cli.command()
def mkdir(path: str) -> None:
    "Create directory."
    os.mkdir(os.path.join(cli.path, path))

@cli.command()
def mkfile(path: str) -> None:
    "Create File."
    with open(os.path.join(cli.path, path)) as f:
        f.close()

@cli.command(alias=["del"])
def delete(path: str) -> None:
    "Remove file or directory."
    os.remove(os.path.join(cli.path, path))

@cli.command(alias=["cp"])
def copy(path1: str, path2: str) -> None:
    "Copy file."
    shutil.copy(os.path.join(cli.path, path1), os.path.join(cli.path, path2))

@cli.command()
def dos(ip: str, port: int, thread: int = 1024, data: int = 1024) -> None:
    "Uses a DOS on the target IP."
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        for i in range(thread):
            executor.submit(utils.send_data, ip, port, data)

cli.run()