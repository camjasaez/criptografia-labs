# from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
    PrivateFormat,
    NoEncryption,
)
from cryptography.hazmat.primitives.asymmetric import ec

private_key = ec.generate_private_key(ec.SECP384R1())

pem = private_key.private_bytes(
    encoding=Encoding.PEM,
    format=PrivateFormat.PKCS8,
    encryption_algorithm=NoEncryption(),
)

with open("keys/private_key.pem", "wb") as f:
    f.write(pem)

public_key = private_key.public_key()

pem = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

with open("keys/public_key.pem", "wb") as f:
    f.write(pem)
