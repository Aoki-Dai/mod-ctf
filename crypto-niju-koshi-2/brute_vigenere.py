import string
import itertools

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


# 一般的な鍵の単語を試す
common_keys = [
    "KEY",
    "SECRET",
    "CIPHER",
    "CRYPTO",
    "PASSWORD",
    "VIGENERE",
    "LATTICE",
    "DOUBLE",
    "GRID",
    "KOSHI",
    "NIJYU",
    "FLAG",
    "PLAYFAIR",
    "HILL",
    "AFFINE",
    "CAESAR",
    "ROT",
    "SHIFT",
    "ENCRYPT",
    "DECRYPT",
    "CODE",
    "HIDDEN",
    "SECURITY",
    # 日本語ローマ字
    "NIJU",
    "KOUSHI",
    "KOSI",
    "NIJUU",
    # 他の可能性
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "ABC",
    "AB",
    "TEST",
    "HELLO",
    "WORLD",
]

print("Testing common keys:")
for key in common_keys:
    plaintext = decrypt_vigenere(ciphertext, key)
    # 平文に意味がありそうか簡単にチェック
    # THE, AND, IS, などの一般的な単語が含まれているか
    if (
        "THE" in plaintext
        or "AND" in plaintext
        or "KEY" in plaintext
        or "FLAG" in plaintext
    ):
        print(f"Key '{key}': {plaintext}")
    # あるいは最初の20文字が読みやすそうか
    common_trigrams = [
        "THE",
        "AND",
        "ING",
        "ENT",
        "ION",
        "HER",
        "FOR",
        "THA",
        "NTH",
        "INT",
    ]
    for tri in common_trigrams:
        if tri in plaintext[:30]:
            print(f"Key '{key}' has '{tri}': {plaintext[:50]}...")
            break

print("\n\nAll decryptions for common keys:")
for key in common_keys:
    plaintext = decrypt_vigenere(ciphertext, key)
    print(f"{key:15}: {plaintext[:60]}...")
