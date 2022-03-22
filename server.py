import threading
import socket
from typing import Callable, Dict, List
import dclasses
import server_commands

HOST = '127.0.0.1'
PORT = 9239
ENCODING = 'utf-8'

COMMAND_MAP: Dict[str, Callable[["Server", dclasses.Client, str], None]] = {
    "claim": server_commands.claim,
    "login": lambda server, client, message: None,
}


class Server:
    def __init__(self, host: str, port: int, encoding: str):
        self.encoding = encoding
        self.clients: Dict[str, dclasses.Client] = {}
        self.users: Dict[str, dclasses.User] = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

    def message_client(self, client: dclasses.Client, message: str):
        client.client.send(message.encode(self.encoding))

    def broadcast(self, message: str):
        for client in self.clients.values():
            self.message_client(client=client, message=message)

    def handle_message(self, client: dclasses.Client, message: str):
        if message[0] == "/":
            command = message[1:].split(" ")[0]
            try:
                COMMAND_MAP[command](server=self, client=client, message=message)
            except KeyError:
                self.message_client(client=client, message=f"Unknown command: {command}")
        else:
            message = f"{client.nickname}: {message}"
            self.broadcast(message=message)

    def nick_in_use(self, nickname):
        try:
            self.users[nickname]
            self.clients[nickname]
        except KeyError:
            return False
        else:
            return True

    def listen(self, client: dclasses.Client):
        while True:
            try:
                message = client.client.recv(1024).decode(self.encoding)
                self.handle_message(client=client, message=message)
            except Exception as e:
                client.client.close()
                del self.clients[client.nickname]

                print(f"Client (nick {client.nickname}) disconnected.")
                self.broadcast(f"{client.nickname} left the chat")
                break

    def start(self):
        while True:
            client, address = self.server.accept()
            print(f"{str(address)} has connected.")

            client.send('NICK'.encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")

            if self.nick_in_use(nickname):
                client.send('Nick in use'.encode("utf-8"))
                client.send('DISCONNECT'.encode("utf-8"))
                return

            client_obj = dclasses.Client(client=client, address=address, nickname=nickname)
            self.clients[client_obj.nickname] = client_obj

            print(f"{str(address)} identified as {nickname}.")

            self.broadcast(f"{nickname} has joined the chat!")
            self.message_client(client=client_obj, message="Connected to the server")

            handle_thread = threading.Thread(target=self.listen, args=(client_obj,))
            handle_thread.start()


if __name__ == "__main__":
    server = Server(host=HOST, port=PORT, encoding=ENCODING)
    server.start()
