import string

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ciphertext = ciphertext.replace(" ", "")


def decrypt_vigenere(ciphertext, key):
    key = key.upper()
    plaintext = []
    key_idx = 0
    for char in ciphertext:
        if char in string.ascii_uppercase:
            shift = ord(key[key_idx % len(key)]) - ord("A")
            decrypted_char = chr((ord(char) - ord("A") - shift + 26) % 26 + ord("A"))
            plaintext.append(decrypted_char)
            key_idx += 1
        else:
            plaintext.append(char)
    return "".join(plaintext)


# 外側の暗号を解読
outer_decrypted = decrypt_vigenere(ciphertext, "CRYPTO")
print("外側の暗号を解読:")
print(outer_decrypted)
print()

# 読みやすく区切る
message = "CONGRATULATIONS YOU HAVE SUCCESSFULLY DECODED THE OUTER ENCRYPTION THE KEY IS MONARCHY"
print("メッセージ:")
print(message)
print()

# 残りの暗号文（内側の暗号）を抽出
# "THE KEY IS MONARCHY" の後の部分
inner_cipher_start = outer_decrypted.find("MONARCHY") + len("MONARCHY")
inner_ciphertext = outer_decrypted[inner_cipher_start:]
print("内側の暗号文:")
print(inner_ciphertext)
print(f"長さ: {len(inner_ciphertext)}")
