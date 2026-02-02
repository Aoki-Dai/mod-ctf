import string

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
clean_text = ciphertext.replace(" ", "")

# 1. Outer Cipher: Rail Fence (2 Rails)
# Split into two halves.
mid = (len(clean_text) + 1) // 2
first_part = clean_text[:mid]
second_part = clean_text[mid:]

rf2_decoded = ""
for i in range(len(second_part)):
    rf2_decoded += first_part[i] + second_part[i]
if len(first_part) > len(second_part):
    rf2_decoded += first_part[-1]

print(f"--- Outer Cipher (Rail Fence 2) Result ---\n{rf2_decoded[:60]}...")


# 2. Inner Cipher: Vigenère
def vigenere_decrypt(text, key):
    key = key.upper()
    pt = ""
    key_idx = 0
    for char in text:
        if char in string.ascii_uppercase:
            shift = ord(key[key_idx % len(key)]) - ord("A")
            pt += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            key_idx += 1
        else:
            pt += char
    return pt


keys_to_try = [
    "EFFECTIVE",
    "EFFECTIVEKEY",
    "EFFECT",
    "KEY",
    "EFFECTIVEFLOW",
    "EFFECTIVELOWKEY",
    "LOWKEYEFFECTIVE",
    "GRID",
    "DOUBLELATTICE",
]

print("\n--- Inner Cipher (Vigenère) Attempts ---")
for k in keys_to_try:
    dec = vigenere_decrypt(rf2_decoded, k)
    print(f"\nKey: {k}")
    print(f"Result: {dec}")
    if "FLAG" in dec or "Key" in dec:  # basic check, though output is all caps
        print(">>> POTENTIAL MATCH <<<")
