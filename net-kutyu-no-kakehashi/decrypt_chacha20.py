#!/usr/bin/env python3
import base64

# ChaCha20 parameters
key = b"PLANT_ChaCha20_SecretKey_2026!!"  # 32 bytes
nonce = b"PLC_N0nc3_!!"  # 12 bytes

# Encrypted password (base64 encoded)
encrypted_b64 = "RUgSWSnENkGwF5XxpYJDN3TkPAVEsEiOmS8ys6tj"
encrypted = base64.b64decode(encrypted_b64)

print(f"Key: {key}")
print(f"Key length: {len(key)} bytes")
print(f"Nonce: {nonce}")
print(f"Nonce length: {len(nonce)} bytes")
print(f"Encrypted (base64): {encrypted_b64}")
print(f"Encrypted (hex): {encrypted.hex()}")
print(f"Encrypted length: {len(encrypted)} bytes")

# Manual ChaCha20 implementation
def rotl32(v, c):
    return ((v << c) | (v >> (32 - c))) & 0xFFFFFFFF

def quarter_round(state, a, b, c, d):
    state[a] = (state[a] + state[b]) & 0xFFFFFFFF
    state[d] ^= state[a]
    state[d] = rotl32(state[d], 16)
    
    state[c] = (state[c] + state[d]) & 0xFFFFFFFF
    state[b] ^= state[c]
    state[b] = rotl32(state[b], 12)
    
    state[a] = (state[a] + state[b]) & 0xFFFFFFFF
    state[d] ^= state[a]
    state[d] = rotl32(state[d], 8)
    
    state[c] = (state[c] + state[d]) & 0xFFFFFFFF
    state[b] ^= state[c]
    state[b] = rotl32(state[b], 7)

def chacha20_block(key, counter, nonce):
    constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    
    key_words = []
    for i in range(8):
        key_words.append(int.from_bytes(key[i*4:(i+1)*4], 'little'))
    
    nonce_words = []
    for i in range(3):
        nonce_words.append(int.from_bytes(nonce[i*4:(i+1)*4], 'little'))
    
    state = constants + key_words + [counter] + nonce_words
    working_state = state.copy()
    
    for _ in range(10):
        quarter_round(working_state, 0, 4, 8, 12)
        quarter_round(working_state, 1, 5, 9, 13)
        quarter_round(working_state, 2, 6, 10, 14)
        quarter_round(working_state, 3, 7, 11, 15)
        quarter_round(working_state, 0, 5, 10, 15)
        quarter_round(working_state, 1, 6, 11, 12)
        quarter_round(working_state, 2, 7, 8, 13)
        quarter_round(working_state, 3, 4, 9, 14)
    
    result = []
    for i in range(16):
        result.append((working_state[i] + state[i]) & 0xFFFFFFFF)
    
    output = b''
    for word in result:
        output += word.to_bytes(4, 'little')
    
    return output

def chacha20_decrypt(key, nonce, ciphertext):
    plaintext = b''
    num_blocks = (len(ciphertext) + 63) // 64
    
    for block_counter in range(num_blocks):
        keystream = chacha20_block(key, block_counter, nonce)
        start = block_counter * 64
        end = min(start + 64, len(ciphertext))
        block_data = ciphertext[start:end]
        
        for i, byte in enumerate(block_data):
            plaintext += bytes([byte ^ keystream[i]])
    
    return plaintext

# Decrypt with manual implementation
print("\n--- Manual ChaCha20 ---")
decrypted = chacha20_decrypt(key, nonce, encrypted)
print(f"Decrypted: {decrypted}")
try:
    print(f"Decrypted (as string): {decrypted.decode('utf-8')}")
except:
    print(f"Decrypted (as string): {decrypted.decode('utf-8', errors='replace')}")
