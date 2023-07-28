import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

# from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
)


def start_client():
    host = "localhost"
    port = 1234

    with open("keys/private_key.pem", "rb") as f:
        private_key_pem = f.read()

    private_key = load_pem_private_key(private_key_pem, password=None)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Conectado al servidor...")

    while True:
        message = input("Escribe un mensaje: ")
        msg_encoded = message.encode()
        signature = private_key.sign(msg_encoded, ec.ECDSA(hashes.SHA256()))
        client_socket.send(msg_encoded + b"\0" + signature)

        if message.lower() == "salir":
            break

    client_socket.close()


if __name__ == "__main__":
    start_client()
