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


def explore():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(recv_until(s, b"> ").decode())

    # Alloc A
    print("Sending 1 (Alloc A)")
    s.sendall(b"1\n")
    print(recv_until(s, b": ").decode())  # Expect Size

    print("Sending 32 (Size)")
    s.sendall(b"32\n")
    print(recv_until(s, b"> ").decode())  # Expect Menu

    # Alloc B
    print("Sending 2 (Alloc B)")
    s.sendall(b"2\n")
    # Does it ask for size or name?
    # I'll just read until a prompt or menu
    out = recv_until(s, b": ")  # might be "name: "
    print(out.decode())

    if b"name" in out:
        print("Sending BName")
        s.sendall(b"BName\n")
        print(recv_until(s, b"> ").decode())
    else:
        # Maybe it didn't ask for name?
        # Check if we are back at menu
        if b"> " in out:
            pass  # back at menu
        else:
            # Maybe wait for >
            print(recv_until(s, b"> ").decode())

    # Show B
    print("Sending 7 (Show B)")
    s.sendall(b"7\n")
    print(recv_until(s, b"> ").decode())

    # Show A
    print("Sending 6 (Show A)")
    s.sendall(b"6\n")
    print(recv_until(s, b"> ").decode())

    # Show address of debug_function?
    # Not sure how to get it yet.

    s.close()


if __name__ == "__main__":
    explore()
