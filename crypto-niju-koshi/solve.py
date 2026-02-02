import string
import collections

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
clean_text = ciphertext.replace(" ", "")


# Function to calculate Index of Coincidence (IC)
def get_ic(text):
    freq = collections.Counter(text)
    n = len(text)
    if n < 2:
        return 0
    ic = 0
    for char_count in freq.values():
        ic += char_count * (char_count - 1)
    return ic / (n * (n - 1))


# Function to solve Vigenere given text and period
def solve_vigenere(text, period):
    key_chars = []
    for i in range(period):
        sub_text = text[i::period]
        # Calculate letter frequencies for this sub-text
        freq = collections.Counter(sub_text)
        # Find the most frequent letter
        if not freq:
            key_chars.append("A")  # Default if sub_text is empty
            continue
        most_frequent_char = max(freq, key=freq.get)
        # Assuming 'E' is the most frequent letter in English plaintext
        # Shift = (most_frequent_char - 'E') mod 26
        shift = (ord(most_frequent_char) - ord("E")) % 26
        key_chars.append(chr(ord("A") + shift))

    key = "".join(key_chars)

    # Decrypt using the guessed key
    decrypted_text = ""
    for i, char in enumerate(text):
        shift = ord(key[i % len(key)]) - ord("A")
        decrypted_text += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))

    return f"Guessed Key: {key}\nDecrypted Text: {decrypted_text}"


print(f"Len: {len(clean_text)}")

print("\n--- Caesar Cipher (ROT-N) ---")
for shift in range(1, 26):
    decoded = ""
    for char in clean_text:
        if char in string.ascii_uppercase:
            decoded += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
        else:
            decoded += char
    print(f"Shift {shift:02}: {decoded[:60]}...")

print("\n--- Vigenere Decrypt with Period 19 (Best IC) ---")
# Best key guess from previous run: KCTDVKBREHFEURZIGKC
key = "KCTDVKBREHFEURZIGKC"
pt = ""
for i, char in enumerate(clean_text):
    shift = ord(key[i % len(key)]) - ord("A")
    pt += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
print(f"PT (Period 19): {pt}")

print("\n--- Analyze Rail Fence 2 Raw Output ---")
# Manually construct Rail Fence 2 Decrypt
# Split into 2 halves (Ceil/Floor)
mid = (len(clean_text) + 1) // 2  # 69
first = clean_text[:mid]
second = clean_text[mid:]
rf2_res = ""
for i in range(len(second)):
    rf2_res += first[i] + second[i]
if len(first) > len(second):
    rf2_res += first[-1]

print(f"RF2: {rf2_res}")
print(f"IC of RF2: {get_ic(rf2_res)}")

print("\n--- Solve Vigenere on RF2 ---")
# Try Period 1-20 on RF2
best_p_rf2 = 0
best_ic_rf2 = 0
for p in range(1, 21):
    avg = 0
    for i in range(p):
        avg += get_ic(rf2_res[i::p])
    avg /= p
    print(f"RF2 Period {p}: IC={avg:.4f}")
    if avg > best_ic_rf2:
        best_ic_rf2 = avg
        best_p_rf2 = p

print(f"Best Period RF2: {best_p_rf2}")
print(solve_vigenere(rf2_res, best_p_rf2))

# Also try splitting by even/odd (Reverse Rail Fence 2?)
# Actually clean_text IS the Reverse Rail Fence result if we just read it linearly?
# No, "Encryption is Rail Fence". "Decryption is undoing it".
# If ciphertext = RailFence(Plain), then Decrypt(Cipher) = Plain.
# We generated RF2 output above.
