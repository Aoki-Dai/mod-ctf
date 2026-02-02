from pwn import *
import sys

# Set up connection
host = '10.2.0.5'
port = 10004

def start():
    return remote(host, port)

p = start()

def allocate_a():
    p.sendlineafter(b'> ', b'1')

def allocate_b():
    p.sendlineafter(b'> ', b'2')

def free_a():
    p.sendlineafter(b'> ', b'3')

def free_b():
    p.sendlineafter(b'> ', b'4')

def write_a(data):
    p.sendlineafter(b'> ', b'5')
    p.sendlineafter(b'Data: ', data)

def show_a():
    p.sendlineafter(b'> ', b'6')
    return p.recvline()

def show_b():
    p.sendlineafter(b'> ', b'7')
    return p.recvline()

# Scenario 1: Allocate A and B, Show B
print("--- Scenario 1 ---")
allocate_a()
allocate_b()
print("Allocated A and B")
res = show_b()
print(f"Show B: {res}")

# check if we can write to A and see if it overflows to B?
# Or check Use After Free.
# Free A, then Write A?
print("--- Scenario 2: UAF test ---")
free_a()
print("Freed A")
try:
    write_a(b"test_uaf")
    print("Write A after free succeeded (UAF exists!)")
    res_a = show_a()
    print(f"Show A after free: {res_a}")
except Exception as e:
    print(f"Write A after free failed: {e}")

p.close()
