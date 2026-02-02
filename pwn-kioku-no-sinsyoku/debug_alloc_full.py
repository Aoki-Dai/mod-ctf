import socket
import time

host = "10.2.0.5"
port = 10004


def get_response(s):
    time.sleep(1)
    try:
        data = s.recv(4096)
        return data.decode(errors="ignore")
    except Exception as e:
        return str(e)


def analyze():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("Initial:", get_response(s))

    # Alloc A
    print("--- Alloc A ---")
    s.sendall(b"1\n")
    print("Sent 1. Resp:", get_response(s))  # Size

    s.sendall(b"32\n")
    print("Sent 32. Resp:", get_response(s))  # Name?

    s.sendall(b"AAAA\n")
    print("Sent AAAA. Resp:", get_response(s))  # Done?

    # Alloc B
    print("--- Alloc B ---")
    s.sendall(b"2\n")
    print("Sent 2. Resp:", get_response(s))  # Name?

    s.close()


if __name__ == "__main__":
    analyze()
