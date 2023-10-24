import PyCLI
import requests
import platform
import os
import colorama
import ddos
import geocoder
import socket
import IpLogger
import concurrent.futures
from hashlib import sha256
import random
import string

all_chars = string.ascii_letters + string.digits + string.punctuation
my_ip = requests.get('https://httpbin.org/ip').json()['origin']
scanned_port = 0

GUI = f"""{colorama.Fore.YELLOW}                .                       
{colorama.Fore.YELLOW}             .~5P.                      
{colorama.Fore.YELLOW}           :JB&&G:                      
{colorama.Fore.YELLOW}         ^YB&&&#P^                      
{colorama.Fore.YELLOW}       :JGB####B5!                      
{colorama.Fore.YELLOW}     .~5GBBGGGGG5J:                     
{colorama.Fore.YELLOW}    .~5PPPPPP5555J?:                    
{colorama.Fore.YELLOW}    .J555YYYYJJJJJ??!:                  8888888 8888888b. {colorama.Fore.LIGHTRED_EX}      88888888888                888          
{colorama.Fore.YELLOW}    .!5YYJJ???77777!!7!^.                 888   888   Y88b{colorama.Fore.LIGHTRED_EX}          888                    888         
{colorama.Fore.LIGHTRED_EX}   !7:~{colorama.Fore.YELLOW}JJJ??777!!!~~~~~!!^.               888   888    888{colorama.Fore.LIGHTRED_EX}          888                    888         
{colorama.Fore.LIGHTRED_EX}  ^PP57{colorama.Fore.YELLOW}^~7?77!!!~~~^^^~~~!!^              888   888   d88P{colorama.Fore.LIGHTRED_EX}          888   .d88b.   .d88b.  888 .d8888b 
{colorama.Fore.LIGHTRED_EX} .Y5555Y!:{colorama.Fore.YELLOW}^!77!~~~^^^^^^~~!!!.            888   8888888P" {colorama.Fore.LIGHTRED_EX}          888  d88""88b d88""88b 888 88K     
{colorama.Fore.LIGHTRED_EX} !5YJJJJJ?~.{colorama.Fore.YELLOW}.^!!~~^^^^~~~~!!7?:           888   888       {colorama.Fore.LIGHTRED_EX}          888  888  888 888  888 888 "Y8888b.
{colorama.Fore.LIGHTRED_EX}.JJ???777777: {colorama.Fore.YELLOW}.^!!~~~~~~!!!77?7           888   888       {colorama.Fore.LIGHTRED_EX}          888  Y88..88P Y88..88P 888      X88
{colorama.Fore.LIGHTRED_EX}:J?77!!!~~~!!~. {colorama.Fore.YELLOW}.~7!!!!!7777?J7         8888888 888       {colorama.Fore.LIGHTRED_EX}          888   "Y88P"   "Y88P"  888  88888P'  
{colorama.Fore.LIGHTRED_EX}.??7!!~~^^^^~!!. {colorama.Fore.YELLOW}.~?77777???J?.         
{colorama.Fore.LIGHTRED_EX} ^?77!~~^^^~~!7^ {colorama.Fore.YELLOW}.^?????JJJJ!.          
{colorama.Fore.LIGHTRED_EX}  .~777!!!!!!!7! {colorama.Fore.YELLOW}.~JJJJYYJ!.            
{colorama.Fore.LIGHTRED_EX}    .:!7?7777??~ {colorama.Fore.YELLOW}.!YY5YJ~.              
{colorama.Fore.LIGHTRED_EX}       .^!?JJJY^ {colorama.Fore.YELLOW}.J5J!:                 
{colorama.Fore.LIGHTRED_EX}          .:!JY. {colorama.Fore.YELLOW}.~.                   """

match platform.system():
    case "Windows": clear_cmd = "cls"
    case "Lynux": clear_cmd = "reset"
    case "Darwin": clear_cmd = "clear"

colorama.init()
print(colorama.Fore.RED)
ports = []

print(GUI)

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

@cli.command(alias=["cfm"])
def chiffrement(path):
    file = path.split("/")[-1]
    path = path.split("/")[::-1]
    key = "".join(random.choice(all_chars) for x in range(random.randint(26, 32)))
    print(f"Key: {key}")

@cli.command(alias=[clear_cmd])
def clear() -> None:
    "Reset the terminal display."
    os.system(clear_cmd)
    print(GUI)

@cli.command(name="ddos")
def ddos_cmd(ip: str, port: int) -> None:
    "Search all opened port of IPv4 adresse or domain name and send data in opened port."
    ddos.main(ip=ip, port=port)

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

@cli.command(alias=['cfg'])
def config():
    "Open the settings file."
    os.system("settings.json")

cli.run()
#ajouter un systeme de save des url iplogger
#ajouter une commande pour afficher la liste des url iplogger
#faire un systeme d'option avec un fichier json

#lcD<,c]|.g3gYLj:Uq'Ta#18