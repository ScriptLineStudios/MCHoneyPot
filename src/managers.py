import multiprocessing
from src.bot import Bot
from src.server import Server
from src.config import config


class ServerManager:
    def __init__(self, ports):
        self.ports = ports
        self.message_queue = multiprocessing.Queue()

    def start_server(self, port):
        server = Server(self, port)
        server.start()

    def start(self):
        for port in self.ports:
            process = multiprocessing.Process(target=self.start_server, args=(int(port),))
            process.start()


class Manager:
    def __init__(self, ports=[25565]):
        self.server_manager = ServerManager(ports)
        self.bot = Bot(self.server_manager)

    def start(self):
        self.bot.start()
        self.server_manager.start()
