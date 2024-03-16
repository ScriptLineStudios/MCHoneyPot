import logging
import os
import json
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def handle_config():
    with open("config.json", "w") as f:
        f.write(
            json.dumps(
                {
                    "discord_token": "",
                    "abuseipdb_token": "",
                    "mongo_uri": "",
                    "database_name": "",
                }
            )
        )
    logging.info("No config file found! Please fill in the one we just created.")
    exit(1)

def usage():
    print("Usage: python run.py [LIST OF PORTS]")
    print("     Example: python run.py 25565 25566 25567")
    exit(0)

if __name__ == "__main__":
    if not os.path.exists("config.json"):
        handle_config()
    if len(sys.argv) <= 1:
        usage()

    from src.managers import Manager

    Manager(sys.argv[1:]).start()
