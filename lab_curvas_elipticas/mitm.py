# mitm.py
import socket
import random


def start_mitm():
    host = "localhost"
    client_port = 1234  # El puerto que MitM escucha para el cliente
    server_port = 4322  # El puerto que MitM se conecta al servidor

    # Configura el socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, client_port))
    server_socket.listen(1)
    print(f"Escuchando en el puerto {client_port} para el cliente")

    # Configura el socket del cliente para conectarse al servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, server_port))
    print(f"Conectado al servidor en el puerto {server_port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Cliente conectado desde {addr}")

        while True:
            print("Esperando mensaje del cliente...")
            # Recibe el dato del cliente
            data = conn.recv(1024)
            if not data:
                print("Cliente desconectado")
                break

            try:
                print(f"Recibido del cliente: {data.decode()}")
            except UnicodeDecodeError:
                print(f"Recibido del cliente (datos binarios): {data.hex()}")

            # Aleatoriamente modifica el dato
            if random.randint(1, 10) == 1:  # 10% de probabilidad de modificar el dato
                data = bytearray(data)
                data[0] = 0  # Cambia el primer byte a 0
                print("Mensaje modificado antes de enviar al servidor")

            # Envia el dato al servidor
            client_socket.send(data)

            # Recibe el dato del servidor
            data = client_socket.recv(1024)
            if not data:
                print("Servidor desconectado")
                break

            try:
                print(f"Recibido del servidor: {data.decode()}")
            except UnicodeDecodeError:
                print(f"Recibido del servidor (datos binarios): {data.hex()}")

            # Aleatoriamente modifica el dato
            if random.randint(1, 10) == 1:  # 10% de probabilidad de modificar el dato
                data = bytearray(data)
                data[0] = 0  # Cambia el primer byte a 0
                print("Mensaje modificado antes de enviar al cliente")

            # Envia el dato al cliente
            print("Enviando al cliente...")
            conn.send(data)

        print("Cliente desconectado")
        conn.close()


if __name__ == "__main__":
    start_mitm()
