import json

class Config:
    def __init__(self):
        with open("config.json", "r") as f:
            self.raw = json.load(f)
        for config in self.raw:
            setattr(self, config, self.raw[config])

config = Config()