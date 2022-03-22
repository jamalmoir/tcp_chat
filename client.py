import socket
import threading

HOST = '127.0.0.1'
PORT = 9239
ENCODING = 'utf-8'


class Client:
    def __init__(self, host, port, encoding, nickname):
        self.encoding = encoding
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode(self.encoding)

                if message == "NICK":
                    self.client.send(self.nickname.encode(self.encoding))
                else:
                    print(message)
            except Exception as e:
                print(f"An error occurred: {e}")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode(self.encoding))

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    nickname = input("Enter a nickname: ")
    client = Client(host=HOST, port=PORT, encoding=ENCODING, nickname=nickname)
    client.start()
