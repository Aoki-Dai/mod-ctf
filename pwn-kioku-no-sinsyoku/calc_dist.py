import socket
import time
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
    # Regex for "Label: 0x..."
    m = re.search(f"{label}: (0x[0-9a-f]+)", out)
    if m:
        return int(m.group(1), 16)
    return None


def calc():
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

    # Show A
    s.sendall(b"6\n")
    out_a = recv_until(s, b"> ").decode(errors="ignore")
    data_a = parse_addr(out_a, "Data address")
    print(f"Data A: {hex(data_a) if data_a else 'None'}")

    # Show B
    s.sendall(b"7\n")
    out_b = recv_until(s, b"> ").decode(errors="ignore")
    obj_b = parse_addr(out_b, "Object address")
    print(f"Obj B: {hex(obj_b) if obj_b else 'None'}")

    if data_a and obj_b:
        dist = obj_b - data_a
        print(f"Distance: {dist} bytes")

    s.close()


if __name__ == "__main__":
    calc()
