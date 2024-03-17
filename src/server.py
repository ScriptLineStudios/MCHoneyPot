import socket
import json
import threading
import multiprocessing
import logging
import queue
import time
import abuseipdb
import quarry

from src.bot import Bot
from src.details import ServerDetails
from src.database import Database
from quarry.types.buffer import Buffer
from src.config import config
from mojang import API
from get_ipinfo import ip_details


class Server:
    def __init__(self, manager, port):
        self.manager = manager
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("", self.port))
        self.server.listen(-1)
        self.details = ServerDetails()
        self.data_buffer = Buffer()
        self.lock = threading.Lock()
        self.states = {}
        self.packets = queue.Queue()
        self.db = Database()
        self.api = API()
        self.reporter = abuseipdb.AbuseIpDb(config.abuseipdb_token)
        self.packet_handles = {
            0: {
                -1: self.handle_status_request,
                2: self.handle_play_request,
            },
            1: {1: self.handle_ping_request},
        }

    def handle_ping(self, addr):
        details = ip_details(addr[0])
        self.db.insert_ping(
            {
                "ip": addr[0],
                "time": time.time(),
                "city": details["City:"],
                "state": details["State:"],
                "country": details["Country:"],
                "gps": details["GPS:"],
                "zip": details["ZIP:"],
                "isp": details["ISP:"],
            }
        )

        try:
            report = self.reporter.report(
                ip_address=addr[0],
                categories=(14),
                comment="Port scanning for vulnerable Minecraft servers.",
            )
            self.db.insert_report(report)
        except TypeError:
            pass

        if int(time.time()) % 15 == 0:
            logging.info("Sampling new usernames")
            self.details.regenerate_online_players()

    def handle_status_request(self, buffer, conn, addr):
        buffer.unpack_varint()
        buffer.unpack_string()
        buffer.unpack("H")
        next_state = buffer.unpack_varint()
        self.states[conn] = next_state

        return_buffer = b""
        return_buffer += Buffer.pack_varint(0)
        return_buffer += Buffer.pack_string(json.dumps(self.details.data))
        conn.sendall(Buffer.pack_varint(len(return_buffer)))
        conn.sendall(return_buffer)
        logging.info(f"Connection at {addr} sent a status packet")
        self.manager.message_queue.put(
            f"New ping on port `{self.port}` from: <`{addr}`>"
        )
        threading.Thread(target=self.handle_ping, args=(addr,)).start()

    def handle_play_request(self, buffer, conn, addr):
        name = buffer.unpack_string()
        self.manager.message_queue.put(
            f"New join attempt on port `{self.port}` from: <`{addr}`> with username: <`{name}`>"
        )
        logging.info(
            f"Connection at {addr} sent a play packet. Their username is {name}"
        )
        self.states[conn] - 1

        uuid = None
        try:
            uuid = self.api.get_uuid(name)
        except mojang.errors.NotFound:
            pass

        self.db.insert_join({"ip": addr[0], "name": name, "uuid": uuid})

    def handle_ping_request(self, buffer, conn, addr):
        long = buffer.read()
        return_buffer = b""
        return_buffer += Buffer.pack_varint(1)
        return_buffer += bytearray(long)

        conn.sendall(Buffer.pack_varint(9))
        conn.sendall(return_buffer)
        logging.info(f"Connection at {addr} sent a ping packet")
        self.states[conn] = -1

    def handle_client(self, conn, addr):
        while True:
            data = conn.recv(1)
            if not data:
                break
            try:
                length = Buffer(data).unpack_varint()
            except quarry.types.buffer.BufferUnderrun:
                conn.close()
                break

            if length <= 1:
                continue

            buffer = b""
            while len(buffer) != length:
                buffer += conn.recv(1)

            self.packets.put(Buffer(buffer))

            buffer = self.packets.get()
            buffer.save()
            buffer.restore()

            _id = buffer.unpack_varint()
            logging.info(
                f"Received Minecraft protocol packet from {addr} with ID {_id}"
            )
            self.packet_handles.get(_id).get(self.states[conn])(buffer, conn, addr)
        logging.info(f"Closing connection with {addr}")
        del self.states[conn]

    def start(self):
        while True:
            try:
                conn, addr = self.server.accept()
                self.states[conn] = -1
                logging.info(f"Got a new connection from: {addr}")
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
            except KeyboardInterrupt:
                exit()
