import threading
import socket
import dataclasses
from typing import Any

HOST = '127.0.0.1'
PORT = 9239
ENCODING = 'utf-8'


@dataclasses.dataclass(frozen=True)
class Client:
    client: Any
    address: str
    nickname: str


class Server:
    def __init__(self, host: str, port: int, encoding: str):
        self.encoding = encoding
        self.clients: list[Client] = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

    def broadcast(self, message: str):
        for client in self.clients:
            client.client.send(message.encode(self.encoding))

    def handle(self, client: Client):
        while True:
            try:
                message = client.client.recv(1024).decode(self.encoding)
                self.broadcast(message)
            except Exception as e:
                client.client.close()
                self.clients.remove(client)

                print(f"Client disconnected: {e}")
                self.broadcast(f"{client.nickname} left the chat")

    def start(self):
        while True:
            client, address = self.server.accept()
            print(f"{str(address)} has connected.")

            client.send('NICK'.encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")

            client_obj = Client(client=client, address=address, nickname=nickname)
            self.clients.append(client_obj)

            print(f"{str(address)} identified as {nickname}.")

            self.broadcast(f"{nickname} has joined the chat!")
            client.send("Connected to the server".encode("utf-8"))

            thread = threading.Thread(target=self.handle, args=(client_obj,))
            thread.start()


if __name__ == "__main__":
    server = Server(host=HOST, port=PORT, encoding=ENCODING)
    server.start()
