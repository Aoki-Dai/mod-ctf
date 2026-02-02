#!/usr/bin/env python3
import socket
import threading
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor

FLAG = os.environ.get('FLAG', '')
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 10007))

MAX_WORKERS = 100
MAX_INPUT_LENGTH = 10

connection_times = {}
connection_lock = threading.Lock()

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

def handle_client(conn, addr):
    client_ip = addr[0]

    with connection_lock:
        now = time.time()
        expired = [k for k, v in connection_times.items() if now - v > 60]
        for k in expired:
            del connection_times[k]
        if client_ip in connection_times:
            if now - connection_times[client_ip] < 10:
                try:
                    conn.sendall(b"Rate limited. Wait 10 seconds.\n")
                except:
                    pass
                conn.close()
                return
        connection_times[client_ip] = now

    try:
        conn.settimeout(30)
        current_time = int(time.time())
        random.seed(current_time)

        conn.sendall(b"=== Oracle of Numbers ===\n")
        conn.sendall(f"Seed: {current_time}\n".encode())
        conn.sendall(b"Guess my sacred numbers 5 times to reveal the secret.\n\n")

        for i in range(5):
            target = random.randint(1, 100)
            conn.sendall(f"Round {i+1}/5 - Enter your guess (1-100): ".encode())

            try:
                data = conn.recv(1024)
                if not data:
                    return
                data = data.decode('utf-8', errors='ignore').strip()
                if len(data) > MAX_INPUT_LENGTH:
                    conn.sendall(b"Input too long.\n")
                    return
                if not data:
                    conn.sendall(b"Invalid input.\n")
                    return
                guess = int(data)
            except (ValueError, UnicodeDecodeError):
                conn.sendall(b"Invalid input.\n")
                return

            if guess == target:
                conn.sendall(b"Correct!\n")
            else:
                conn.sendall(f"Wrong. The number was {target}.\n".encode())
                return

        conn.sendall(f"The secret is: {FLAG}\n".encode())

    except socket.timeout:
        pass
    except (BrokenPipeError, ConnectionResetError, OSError):
        pass
    finally:
        try:
            conn.close()
        except:
            pass

def main():
    if not FLAG:
        print("WARNING: FLAG is not set")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)
    print("Server started")

    while True:
        try:
            conn, addr = server.accept()
            executor.submit(handle_client, conn, addr)
        except Exception:
            pass

if __name__ == '__main__':
    main()
