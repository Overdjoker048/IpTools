from pycli import *
import requests
import os
import colorama
import geocoder
import socket
import utils
import concurrent.futures
from fake_useragent import UserAgent

os.system("title FireWare")
my_ip = requests.get("https://httpbin.org/ip").json()["origin"]
scanned_port = 0

bdd = utils.BDD()
for nmb, port in enumerate(bdd.info["port"]):
    utils.Logger_link(bdd.info["url"][nmb], port, my_ip).start()
del bdd

prompt_design = colored("\n┌─[", "FF0000")+colored("FireWare", "FFFFF")+colored("]", "FF0000")+colored("@", "FFA000")+colored("[", "FF0000")+colored("{}")+colored("]", "FF0000")+colored(":~\n", "1A1A1A")+colored("└", "FF0000")+colored("[", "FF0000")+colored("{}")+colored("]", "FF0000")+colored(">", "FF0000")+colored(" $ ", "FFA500")
cli = CLI(prompt=prompt_design, anim=True, logs=True, user="Overdjoker")

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
    bdd = utils.BDD()
    if not bdd.exist(port):
        utils.Logger_link(url, port, my_ip).start()
        bdd.add(port, url)
    else:
        print("The port are already used.")
        print(f"Use the remove_link command to remove the URL hosted on port {port}.")

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
        pourcent_display = colorama.Fore.RED+"█"*(pourcent // 5)
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

@cli.command(alias=["gw"])
def get(ip: str, port: int = 80) -> None:
    "Allows you to send a request to an IP address and receive the connection."
    headers = {"User-Agent": UserAgent().random}
    reponse = requests.request("GET", f"http://{ip}:{port}/", headers=headers)
    try:
        if reponse.status_code == 200:
            print(f"{ip} has been successfully downloaded.")
            print(f"[Path] {os.path.dirname(os.path.dirname(__file__))}/{ip}_{port}.html")
            if not os.path.exists("output"):
                os.mkdir("output")
            with open(os.path.join("output", f"{ip}_{port}.html"), "wb") as file:
                file.write(reponse.text.encode("utf-8"))
        else:
            print(f"The query returned an error code: {reponse.status_code}")
    except requests.RequestException as e:
        print(f"An error has occurred: {e}")

@cli.command(alias=["ls"])
def dir():
    "Display all file in directory."
    echo(os.listdir(cli.path), color=(120, 50, 20))

cli.run()