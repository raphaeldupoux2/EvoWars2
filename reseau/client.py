import socket


def start_client():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Connecté au serveur sur {host}:{port}")

    while True:
        data = client_socket.recv(1024)
        print(f"Serveur: {data.decode()}")

        message = input("Client: ")
        client_socket.send(message.encode())

    client_socket.close()


if __name__ == "__main__":
    start_client()
