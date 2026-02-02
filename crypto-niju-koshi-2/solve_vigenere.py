import string

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
ciphertext = ciphertext.replace(" ", "")

english_freqs = {
    "A": 0.08167,
    "B": 0.01492,
    "C": 0.02782,
    "D": 0.04253,
    "E": 0.12702,
    "F": 0.02228,
    "G": 0.02015,
    "H": 0.06094,
    "I": 0.06966,
    "J": 0.00153,
    "K": 0.00772,
    "L": 0.04025,
    "M": 0.02406,
    "N": 0.06749,
    "O": 0.07507,
    "P": 0.01929,
    "Q": 0.00095,
    "R": 0.05987,
    "S": 0.06327,
    "T": 0.09056,
    "U": 0.02758,
    "V": 0.00978,
    "W": 0.02360,
    "X": 0.00150,
    "Y": 0.01974,
    "Z": 0.00074,
}


def score_text(text):
    score = 0
    for char in text:
        if char in english_freqs:
            score += english_freqs[char]
    return score


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


def solve_vigenere_key(ciphertext, key_len):
    key = ""
    for i in range(key_len):
        subtext = ciphertext[i::key_len]
        best_char = ""
        best_score = -1

        # Try all 26 shifts for this position
        for shift in range(26):
            shifted_subtext = ""
            current_shift_char = chr(ord("A") + shift)
            # If we assume the key char is 'A', then we decrypt with shift 0 (Cipher - A).
            # If key is 'B', decrypt with shift 1 (Cipher - B).
            # So we are looking for the Key Char.

            # To 'decrypt', we subtract the key shift.
            # Plain = Cipher - Key.
            # We want Plain to look like English.

            temp_plain = ""
            for c in subtext:
                p_val = (ord(c) - ord("A") - shift + 26) % 26
                temp_plain += chr(p_val + ord("A"))

            # Use Chi-squared or simple dot product
            current_score = score_text(temp_plain)
            if current_score > best_score:
                best_score = current_score
                best_char = current_shift_char
        key += best_char
    return key


lengths_to_try = [6, 9, 12, 18, 19]

for l in lengths_to_try:
    key = solve_vigenere_key(ciphertext, l)
    print(f"Length {l}: Key = {key}")
    print(f"Plaintext sample: {decrypt_vigenere(ciphertext, key)[:50]}...")
    print("-" * 20)
