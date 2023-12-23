import pickle
import socket
import time


class Client:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = '127.0.0.1', 12345
        self.client_socket.connect((self.ip, self.port))

    def receive_world_data(self):
        while True:
            print("Client: Recoit data")
            world_data = self.client_socket.recv(4096)
            print("Client: deserialize data")
            self.game_instance.world = self.deserialize_world(world_data)
            # Ajoutez un délai pour ne pas surcharger la connexion
            time.sleep(0.1)

    def deserialize_world(self, data):
        world = pickle.loads(data)
        return world
