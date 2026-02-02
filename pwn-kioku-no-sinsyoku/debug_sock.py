import socket
import time

host = "10.2.0.5"
port = 10004


def get_response(s):
    time.sleep(1)  # wait for response
    try:
        data = s.recv(4096)
        return data.decode(errors="ignore")
    except Exception as e:
        return str(e)


def analyze():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print("Initial:", get_response(s))

    print("Sending 1...")
    s.sendall(b"1\n")
    print("Response:", get_response(s))

    print("Sending 2...")
    s.sendall(b"2\n")
    print("Response:", get_response(s))

    print("Sending 7 (Show B)...")
    s.sendall(b"7\n")
    print("Response:", get_response(s))

    s.close()


if __name__ == "__main__":
    analyze()
