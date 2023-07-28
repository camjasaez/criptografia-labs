import socket
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
)


def start_server():
    host = "localhost"
    port = 4322

    with open("keys/public_key.pem", "rb") as f:
        public_key_pem = f.read()

    public_key = load_pem_public_key(public_key_pem)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("El servidor está escuchando en el puerto", port)

    while True:
        conn, addr = server_socket.accept()
        print("Conexión establecida con", addr)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message, signature = data.split(b"\0", 1)
            try:
                public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
                print("Cliente:", message.decode())
            except InvalidSignature:
                print(
                    "Firma inválida. El programa es susceptible a un ataque de hombre en el medio"
                )

            try:
                conn.sendall(data)
            except socket.error as e:
                print(f"Error al enviar la data: {e}")

        print("El cliente se ha desconectado", addr)
        conn.close()


if __name__ == "__main__":
    start_server()
