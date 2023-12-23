import pickle
import socket
import time


class Serveur:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip, self.port = '127.0.0.1', 12345  # 127.0.0.1 correspond à l'ip de l'hote dans lequel le jeu est exécuté
        self.server_socket.bind((self.ip, self.port))  # adresse sera 127.0.0.1:1245
        self.server_socket.listen(1)
        self.client_socket, self.address = None, None

    def accept_connections(self):
        print('Serveur: Waiting for connection...')
        self.client_socket, self.address = self.server_socket.accept()
        print('Serveur: Connection established with', self.address)
        self.send_world_data()

    def send_world_data(self):
        while True:
            world_data = self.serialize_world()
            self.client_socket.send(world_data)
            # Ajoutez un délai pour ne pas surcharger la connexion
            time.sleep(0.1)

    def serialize_world(self):
        world_data = pickle.dumps(self.game_instance.world)
        return world_data
