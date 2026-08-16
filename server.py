import socket

HOST = "0.0.0.0"
PORT = 5000

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen()

connection, address = server_socket.accept()
print("Connected by:", address)

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

metadata_length_bytes = recv_exactly(connection, 4)
metadata_length = int.from_bytes(metadata_length_bytes, "big")
metadata = (recv_exactly(connection, metadata_length)).decode()

filename, file_size = metadata.split(",")
file_size = int(file_size)

received_bytes = 0
with open("Newtest.txt", "wb") as file:
    while received_bytes < file_size:
        chunk = connection.recv(min(2048, file_size - received_bytes))
        if not chunk:
            raise ConnectionError("Connection closed before receiving all data")
        file.write(chunk)
        received_bytes += len(chunk)




print("Metadata length:", metadata_length)
print("Metadata:", metadata)
with open("Newtest.txt", "rb") as file:
    file_content = file.read()
    print("File content:", file_content)

connection.sendall(b"ACK!")
