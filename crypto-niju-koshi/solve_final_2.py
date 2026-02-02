import string

ciphertext = "EFLVK OVLJP MWQEQ NHIJR TTLIE TCHLT WCJNW SEFBT WHJVM JMSTV LRKMR KGDGH JVITR WUDMC TFEYW JZGWK ACTUE DTQHI HUKBU SHBXR YEREZ XHYCS CKYYO GBUZG OZIIL ANXKM YRNEK HU"
clean_text = ciphertext.replace(" ", "")

# Re-run RF2 logic since variables aren't persisted
mid = (len(clean_text) + 1) // 2
first_part = clean_text[:mid]
second_part = clean_text[mid:]

rf2_decoded = ""
for i in range(len(second_part)):
    rf2_decoded += first_part[i] + second_part[i]
if len(first_part) > len(second_part):
    rf2_decoded += first_part[-1]


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


print(f"Outer: {rf2_decoded}")

# Try decrypting the REST of RF2 with "EFFECTIVE".
rf2_rest = rf2_decoded[12:]
print("\n--- Try Decrypting Body of RF2 with EFFECTIVE ---")
dec_body = vigenere_decrypt(rf2_rest, "EFFECTIVE")
print(f"Body: {dec_body[:60]}...")

print("\n--- Try Decrypting RF2 (Whole) with Key=ECFTLFVEKYOW ---")
dec_with_prefix = vigenere_decrypt(rf2_decoded, "ECFTLFVEKYOW")
print(f"PrefixKey: {dec_with_prefix[:60]}...")

print("\n--- Try Decrypting RF2 with Key derived from ECFTLFVEKYOW (EFFECTIVEKEY) ---")
dec_eff = vigenere_decrypt(rf2_decoded, "EFFECTIVEKEY")
print(f"EFFECTIVEKEY: {dec_eff[:60]}...")

print("\n--- Try Decrypting RF2 with Key derived from ECFTLFVEKYOW (EFFECTIVEFLOW) ---")
dec_flow = vigenere_decrypt(rf2_decoded, "EFFECTIVEFLOW")
print(f"EFFECTIVEFLOW: {dec_flow[:60]}...")

# What if 'ECFTLFVEKYOW' is the IV? (Just kidding)
# Check if "EFFECTIVEKEY" appears in the *decryption* of RF2 if we try standard keys?
# No.

# What if we assume "Outer" result IS THE FLAG but encoded?
# `ECFT...` looks like flag value? No.

# Try Key: "TWOSQUARES" ? "NIJUKOUSHI"?
# Try Key: "DOUBLELATTICE"?
