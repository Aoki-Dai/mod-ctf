import socket
import re
import random
import time
import sys

HOST = "10.2.4.10"
PORT = 10007


def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # Receive until prompt
    buffer = ""
    while "Enter your guess" not in buffer:
        data = s.recv(1024).decode()
        if not data:
            break
        buffer += data

    print("Received initial buffer:")
    print(buffer)

    # Extract seed
    match = re.search(r"Seed: (\d+)", buffer)
    if not match:
        print("Could not find seed")
        return

    seed = int(match.group(1))
    print(f"[+] Seed found: {seed}")

    # Initialize random generator with the same seed
    random.seed(seed)

    # Generate the 5 numbers
    # We need to simulate the loop exactly as the server does
    # server:
    # for i in range(5):
    #     target = random.randint(1, 100)
    #     ...

    targets = []
    for _ in range(5):
        targets.append(random.randint(1, 100))

    print(f"[+] Generated targets: {targets}")

    # Send guesses
    for i in range(5):
        guess = targets[i]
        print(f"[-] Sending guess {i + 1}: {guess}")
        s.sendall(f"{guess}\n".encode())

        # Read response
        # Expecting "Correct!\n" and potentially next prompt or flag
        time.sleep(0.5)  # Wait a bit for server response
        res = s.recv(4096).decode()
        print(f"[-] Server response: {res.strip()}")

        if "Correct" not in res:
            print("Something went wrong!")
            break

    # Read remaining if any (Flag)
    s.settimeout(2)
    try:
        while True:
            extra = s.recv(1024).decode()
            if not extra:
                break
            print(f"Extra: {extra.strip()}")
            if "flag" in extra.lower():
                print(f"\n[SUCCESS] FOUND FLAG IN: {extra}")
    except socket.timeout:
        pass

    s.close()


if __name__ == "__main__":
    solve()
