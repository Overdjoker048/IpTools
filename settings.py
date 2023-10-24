import json

class config:
    def __init__(self) -> None:
        self.info = {
            "webhook": "URL",
            "Version": 1.0
        }
        try:
            with open("settings.json", "r+") as file:
                self.info = json.load(fp=file)
        except:
            with open("settings.json", "w+") as file:
                json.dump(self.info, file, indent=2)
    
    def save(self) -> None:
        with open("settings.json", "w+") as file:
                json.dump(self.info, file, indent=2)