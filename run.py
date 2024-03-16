import logging

from src.managers import Manager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)

if __name__ == "__main__":
    Manager().start()
