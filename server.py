import os
import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen()

filename_lock = threading.Lock()


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


def handle_client(connection, address):

    metadata_length_bytes = recv_exactly(connection, 4)
    metadata_length = int.from_bytes(metadata_length_bytes, "big")
    metadata = (recv_exactly(connection, metadata_length)).decode()

    filename, file_size = metadata.split(",")
    file_size = int(file_size)

    with filename_lock:    #We lock the filename to avoid collision when multiple clients are trying the same filename, as there is a brief moment before the file is created where another cient could potentially create the same file
        if os.path.exists(filename):
            number = 1
            name, extension = os.path.splitext(filename)
            candidate_filename = f"{name} ({number}){extension}"

            while os.path.exists(candidate_filename):
                number += 1
                candidate_filename = f"{name} ({number}){extension}"
            filename = candidate_filename

        file = open(filename, "xb")

    transfer_successful = False    
    try:
        received_bytes = 0
        last_printed_percentage = 0
        starting_time = time.time()
        while received_bytes < file_size:
            chunk = connection.recv(min(2048, file_size - received_bytes))

            if not chunk:
                raise ConnectionError("Connection closed before receiving all data")   

            file.write(chunk)
            received_bytes += len(chunk)
            
            percentage = int((received_bytes / file_size) * 100)
            
            if percentage > last_printed_percentage:
                
                print(f"Received: {percentage}%\r", end="", flush=True)
            
                last_printed_percentage = percentage
        ending_time = time.time()
        elapsed_time = ending_time - starting_time
        speed = (file_size / elapsed_time) / (1024 ** 2) #Convert to MB/s
        print(f"Speed: {speed:.2f} MB/s")
        transfer_successful = True

    except ConnectionError:
        transfer_successful = False

    file.close()

    if not transfer_successful:
        if os.path.exists(filename):
            os.remove(filename)
    print()
    if transfer_successful:
        
        print("Successfully received file:", filename)
        print("Metadata length:", metadata_length)
        print("Metadata:", metadata)
        
        connection.sendall(b"ACK!")
    connection.close()


while True:

    connection, address = server_socket.accept()
    print("Connected by:", address)

    thread = threading.Thread(target = handle_client, args = (connection, address))
    thread.start()
    
    