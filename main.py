import ram
import PyCLI
import requests
import os
import colorama
import geocoder
import socket
import utils
import concurrent.futures

my_ip = requests.get('https://httpbin.org/ip').json()['origin']
scanned_port = 0

bdd = utils.BDD()
for nmb, port in enumerate(bdd.info["port"]):
    utils.Logger_link(bdd.info["url"][nmb], port, my_ip).start()
del bdd

prompt_design = f"\n{colorama.Fore.LIGHTRED_EX}┌─[{colorama.Fore.YELLOW}FireWare{colorama.Fore.LIGHTRED_EX}]{colorama.Fore.LIGHTYELLOW_EX}@{colorama.Fore.LIGHTRED_EX}[{colorama.Fore.WHITE}{os.getlogin()}{colorama.Fore.LIGHTRED_EX}]{colorama.Fore.LIGHTBLACK_EX}:~{colorama.Fore.LIGHTRED_EX}\n└─>{colorama.Fore.YELLOW} $ {colorama.Fore.WHITE}"
cli = PyCLI.CLI(prompt=prompt_design, animation=False, logs=False)

@cli.command(alias=["cl"])
def create_link(url: str, port: int) -> None:
    "Create an Iplogger link."
    bdd = utils.BDD()
    if not bdd.exist(port):
        utils.Logger_link(url, port, my_ip).start()
        bdd.add(port, url)
    else:
        print("The port are already used.")
        print(f"Use the remove_link command to remove the URL hosted on port {port}.")
        
@cli.command()
def dos(ip: str, port: int) -> None:
    "Search all opened port of IPv4 adresse or domain name and send data in opened port."
    utils.dos(ip=ip, port=port)

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

@cli.command(alias=["sl"])
def show_link() -> None:
    "Display list of hosted port."
    utils.BDD().display()

@cli.command(alias=["rl"])
def remove_link(port: int) -> None:
    "Remove hosting port of list."
    utils.BDD().remove(port=port)
    print("Restart FireWare for actualise host ports.")

@cli.command(alias=["fo"])
def file_open():
    "Open the file who save all info about iplogger links"
    try:
        with open("iplogger.json", "r+") as file:
            print(file.read())
    except:
        with open("iplogger.json", "w+") as file:
            file.close()

ram(debug=True)
cli.run()