import socket
import time

host = "127.0.0.1"
port = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
for i in range(100):
    time.sleep(1)
    s.send(bytes(f"testdata {i}", encoding="utf-8"))
    res = s.recv(100)
    print(f"Received {res}")
