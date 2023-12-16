import threading

from anew.client import Client
from anew.game_instance import GameInstance
from anew.serveur import Serveur


if __name__ == "__main__":
    game_instance = GameInstance()

    # serveur = Serveur(game_instance)
    # print('serveur pass')
    # thread_serveur = threading.Thread(target=serveur.accept_connections)
    # thread_serveur.daemon = True
    # thread_serveur.start()
    #
    # client = Client(game_instance)
    # thread_client = threading.Thread(target=client.receive_world_data)
    # thread_client.daemon = True
    # thread_client.start()

    game_instance.game()
