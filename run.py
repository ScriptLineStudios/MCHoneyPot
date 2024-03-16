# import src.database

import logging
import os
import json

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s-%(levelname)s: %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)

def handle_config():
    with open("config.json", "w") as f:
        f.write(json.dumps({
            "discord_token": "",
            "abuseipdb_token": "",
            "mongo_uri": "",
            "database_name": ""
        }))
    logging.error("No config file found! Please fill in the one we just created.")            
    exit(1)

if __name__ == "__main__":
    if not os.path.exists("config.json"):
        handle_config()

    from src.managers import Manager
    Manager().start()
