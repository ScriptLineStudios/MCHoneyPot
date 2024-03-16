import requests
import random
import json

with open("data/uuids.txt", "r") as f:
    uuids = f.readlines()


class ServerDetails:
    VERSIONS = [
        ("1.20.4", 765),
        ("1.20.1", 763),
        ("Paper 1.20.4", 765),
        ("1.19.4", 762),
        ("1.19.3", 761),
        ("1.12.2", 340),
    ]
    DESCRIPTIONS = [
        "A Minecraft Server",
        "Welcome!",
        "A Vanilla Minecraft Server powered by Docker",
        "welcome",
    ]

    def __init__(self):
        self.version = random.choice(self.VERSIONS)
        self.max_players = round(random.randrange(10, 100), -1)
        self.online_players = random.randrange(0, self.max_players // 10)
        self.samples = [self.get_sample() for i in range(self.online_players)]
        self.description = random.choice(self.DESCRIPTIONS)
        self.generate_data()

    def generate_data(self):
        self.data = {
            "version": {"name": self.version[0], "protocol": self.version[1]},
            "players": {
                "max": self.max_players,
                "online": self.online_players,
                "sample": self.samples,
            },
            "description": {"text": self.description},
        }

    def regenerate_online_players(self):
        self.online_players = random.randrange(0, self.max_players // 10)
        self.samples = [self.get_sample() for i in range(self.online_players)]
        self.generate_data()

    @staticmethod
    def get_sample():
        uuid = random.choice(uuids).strip()
        name = json.loads(
            requests.get(f"https://api.minetools.eu/uuid/{uuid}").content
        )["name"]
        return {"name": name, "id": uuid}
