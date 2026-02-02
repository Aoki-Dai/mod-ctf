#!/usr/bin/env python3
"""
ML-DSA Nonce Reuse Attack using linear algebra

z = y + c * s1 (polynomial multiplication mod X^256 + 1)
With nonce reuse (same y): dz = dc * s1

Polynomial multiplication (a * b)[k] = sum_{i+j=k} a[i]b[j] - sum_{i+j=k+N} a[i]b[j]

This creates a system of linear equations which we can solve.
"""

import socket
import json
import re
import numpy as np

Q = 8380417
N = 256


def recv_until(sock, delimiter):
    data = b""
    while delimiter not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data.decode()


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("10.2.4.12", 10005))
    return sock


def get_menu(sock):
    return recv_until(sock, b"> ")


def send_choice(sock, choice):
    sock.sendall(f"{choice}\n".encode())


def sign_message(sock, message):
    send_choice(sock, "2")
    recv_until(sock, b": ")
    sock.sendall(f"{message}\n".encode())
    response = recv_until(sock, b"> ")

    z_match = re.search(r"z = (\[\[.*?\]\])", response, re.DOTALL)
    c_match = re.search(r"c = (\[.*?\])\n", response, re.DOTALL)

    if z_match and c_match:
        z = eval(z_match.group(1))
        c = eval(c_match.group(1))
        return {"z": z, "c": c}
    return None


def get_flag(sock, s1):
    send_choice(sock, "4")
    recv_until(sock, b": ")
    sock.sendall(f"{json.dumps(s1)}\n".encode())
    response = recv_until(sock, b"> ")
    return response


def mod_center(x, q=Q):
    r = x % q
    if r > q // 2:
        r -= q
    return r


def build_negacyclic_matrix(c):
    """
    Build the matrix M such that M @ s = c * s (negacyclic polynomial multiplication)
    (c * s)[k] = sum_{i=0}^{k} c[i]*s[k-i] - sum_{i=k+1}^{N-1} c[i]*s[N+k-i]
    """
    M = np.zeros((N, N), dtype=np.int64)
    for k in range(N):
        for i in range(N):
            if i <= k:
                # j = k - i, coefficient is positive
                j = k - i
                M[k, j] = (M[k, j] + c[i]) % Q
            else:
                # j = N + k - i, coefficient is negative (negacyclic)
                j = N + k - i
                M[k, j] = (M[k, j] - c[i]) % Q
    return M


def solve_mod_q(M, b, q=Q):
    """
    Solve M @ x = b (mod q) using Gaussian elimination
    """
    n = M.shape[0]
    # Augment matrix
    aug = np.hstack([M.copy(), b.reshape(-1, 1)])
    aug = aug.astype(object)  # For big integers

    # Forward elimination
    for col in range(n):
        # Find pivot
        pivot_row = None
        for row in range(col, n):
            if aug[row, col] % q != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue  # No pivot in this column

        # Swap rows
        aug[[col, pivot_row]] = aug[[pivot_row, col]]

        # Make pivot 1
        pivot_inv = pow(int(aug[col, col]) % q, -1, q)
        aug[col] = (aug[col] * pivot_inv) % q

        # Eliminate below
        for row in range(col + 1, n):
            if aug[row, col] % q != 0:
                factor = aug[row, col]
                aug[row] = (aug[row] - factor * aug[col]) % q

    # Back substitution
    x = np.zeros(n, dtype=object)
    for col in range(n - 1, -1, -1):
        if aug[col, col] % q == 0:
            x[col] = 0  # Free variable, assume 0
        else:
            x[col] = aug[col, n]
            for j in range(col + 1, n):
                x[col] = (x[col] - aug[col, j] * x[j]) % q
            x[col] = (x[col] * pow(int(aug[col, col]), -1, q)) % q

    return np.array([int(v) for v in x])


def main():
    sock = connect()
    _ = get_menu(sock)
    print("Connected to server")

    # Get two signatures
    print("\n=== Collecting signatures ===")
    signatures = []
    for i in range(2):
        msg = f"msg{i}"
        print(f"Signing: {msg}")
        sig = sign_message(sock, msg)
        if sig:
            signatures.append((msg, sig))

    sig0 = signatures[0][1]
    sig1 = signatures[1][1]

    z0, c0 = sig0["z"], sig0["c"]
    z1, c1 = sig1["z"], sig1["c"]

    # dc = c1 - c0, dz = z1 - z0
    dc = [(c1[j] - c0[j]) for j in range(N)]

    print("\n=== Computing s1 via linear algebra ===")

    s1_recovered = []

    for poly_idx in range(2):
        dz = np.array([(z1[poly_idx][j] - z0[poly_idx][j]) % Q for j in range(N)])

        print(f"\nPolynomial {poly_idx}:")
        print(f"  Building negacyclic multiplication matrix...")

        M = build_negacyclic_matrix(dc)

        print(f"  Solving linear system...")
        s1_poly = solve_mod_q(M, dz, Q)
        s1_poly = [mod_center(int(x), Q) for x in s1_poly]
        s1_recovered.append(s1_poly)

        print(f"  s1[:20]: {s1_poly[:20]}")
        print(f"  s1 range: min={min(s1_poly)}, max={max(s1_poly)}")

    # Try to get flag
    print("\n=== Attempting to get flag ===")
    flag_response = get_flag(sock, s1_recovered)
    print(f"Flag response: {flag_response}")

    sock.close()


if __name__ == "__main__":
    main()
