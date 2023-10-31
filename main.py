import PyCLI
import requests
import os
import colorama
import dos
import geocoder
import socket
import IpLogger
import concurrent.futures
import random
import string

all_chars = string.ascii_letters + string.digits + string.punctuation
my_ip = requests.get('https://httpbin.org/ip').json()['origin']
scanned_port = 0
colorama.init()
ports = []

prompt_design = f"\n{colorama.Fore.LIGHTRED_EX}┌─[{colorama.Fore.YELLOW}IpTools{colorama.Fore.LIGHTRED_EX}]{colorama.Fore.LIGHTYELLOW_EX}@{colorama.Fore.LIGHTRED_EX}[{colorama.Fore.WHITE}{os.getlogin()}{colorama.Fore.LIGHTRED_EX}]{colorama.Fore.LIGHTBLACK_EX}:~{colorama.Fore.LIGHTRED_EX}\n└─>{colorama.Fore.YELLOW} $ {colorama.Fore.WHITE}"
cli = PyCLI.CLI(prompt=prompt_design, animation=False, logs=False)

@cli.command(alias=["cl"])
def create_link(url: str, port: int) -> None:
    "Create an Iplogger link."
    if requests.head(url).status_code != 404:
        if not port in ports:
            IpLogger.Logger_link(url=url, port=port, host_ip=my_ip).start()
            ports.append(port)
        else:
            print("The port are already used.")
    else:
        print("The URL doesn't existe.")

"""@cli.command(alias=["cfm"])
def chiffrement(path):
    file = path.split("/")[-1]
    path = path.split("/")[::-1]
    key = "".join(random.choice(all_chars) for x in range(random.randint(26, 32)))
    print(f"Key: {key}")"""

@cli.command(name="dos")
def dos_cmd(ip: str, port: int) -> None:
    "Search all opened port of IPv4 adresse or domain name and send data in opened port."
    dos.main(ip=ip, port=port)

@cli.command(alias=["glc"])
def geolocate(ip: str) -> None:
    "Geolocate IPv4 adresse or domain name."
    ip = socket.gethostbyname(ip)
    print(f"Localisation: {geocoder.ip(socket.gethostbyname(ip)).city}[{geocoder.ip(socket.gethostbyname(ip)).country}]")

@cli.command(alias=["gip"])
def get_ip(ip: str) -> None:
    "Display the Ipv4 adresse or domain name."
    if ip != socket.gethostbyname(ip):
        print(f"Domain: {socket.gethostbyname(ip)}")

@cli.command(alias=["sp"])
def scan_port(ip: str) -> None:
    global scanned_port
    "Display the Ipv4 adresse of domain name."
    socket.setdefaulttimeout(1)
    opened_port = []
    def scan(ip: str, port: int) -> None:
        global scanned_port
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if scanner.connect_ex((ip, port)) == 0:
            opened_port.append(port)
        scanned_port += 1
        pourcent = int((scanned_port/65535) *100)
        pourcent_display = colorama.Fore.LIGHTRED_EX+"█"*(pourcent // 5)
        unpoucent_display = " "*(20-(pourcent // 5))
        print(f"{pourcent_display}{unpoucent_display}{colorama.Fore.WHITE} {pourcent}/100% {colorama.Fore.YELLOW}{scanned_port}/65535", end="\r")
        scanner.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        for port in range(65535):
            executor.submit(scan, ip, port+1)
    print(" "*60, end="\r")
    for i in opened_port:
        print(f"{colorama.Fore.LIGHTRED_EX}[{colorama.Fore.YELLOW}+{colorama.Fore.LIGHTRED_EX}]{colorama.Fore.WHITE}{ip}:{i}")
    scanned_port = 0

@cli.command(alias=["vsn"])
def version() -> None:
    "Display the version of IP Tool."
    print("Version: 1.0")

cli.run()
#ajouter un systeme de save des url iplogger
#ajouter une commande pour afficher la liste des url iplogger