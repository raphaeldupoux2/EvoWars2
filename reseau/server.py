import socket


def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Serveur en attente de connexion sur {host}:{port}")

    client_socket, addr = server_socket.accept()
    print(f"Connexion établie avec {addr}")

    while True:
        message = input("Serveur: ")
        client_socket.send(message.encode())

        data = client_socket.recv(1024)
        print(f"Client: {data.decode()}")

    client_socket.close()


if __name__ == "__main__":
    start_server()
