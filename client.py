import socket
import os

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

filename = "test.txt"

file_size = os.path.getsize(filename)   

metadata = f"{filename},{file_size}"
metadata_bytes = metadata.encode()

metadata_length = len(metadata_bytes)
metadata_length_bytes = metadata_length.to_bytes(4, "big")

print("Metadata:", metadata)
print("Metadata Bytes:", metadata_bytes)
print("Metadata Length:", metadata_length)
print("Metadata Length Bytes:", metadata_length_bytes)

client_socket.sendall(metadata_length_bytes)
client_socket.sendall(metadata_bytes)

def recv_exactly(connection, number_of_bytes):
    received = 0
    chunks = []

    while received < number_of_bytes:
        chunk = connection.recv(number_of_bytes - received)
        print("Received:", chunk)
        if not chunk:
            raise ConnectionError("Connection closed before receiving all data")
        
        received += len(chunk)
        chunks.append(chunk)

    return b"".join(chunks)

sent = 0
with open(filename, "rb") as file:
    while sent < file_size:
        chunk = file.read(min(2048, file_size - sent))
        if not chunk:
            raise IOError("File ended before the expected file size was read")

        client_socket.sendall(chunk)
        sent += len(chunk)
        

        

ack = (recv_exactly(client_socket, 4))
if ack == b"ACK!":
    print("File sent successfully and acknowledged by the server.")
client_socket.close()