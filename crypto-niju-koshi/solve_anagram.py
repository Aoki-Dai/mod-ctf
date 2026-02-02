# The result `RHGGYBUS...` is still not clear.
# Maybe the key `ECFTLFVEKYOW` needs to be anagrammed to `EFFECTIVEKEY`?
# Note `ECFTLFVEKYOW` -> `EFFECTIVEKEY` + `OW`.
# `OW` remaining. "WO"?
# "TWO"?
# W and O are in the string.
# Maybe `EFFECTIVE TWO KEY`? No.
# `EFFECTIVE KEY TWO`?
# `EFFECTIVE KEY FLOW`?
#
# Let's try `EFFECTIVEKEY` on the WHOLE `RF2` string (including the prefix).
# Or just the body.

import string

rf2_decoded = "ECFTLFVEKYOWVJLZJGPWMKWAQCETQUNEHDITJQRHTITHLUIKEBTUCSHHLBTXWRCYJENRWESZEXFHBYTCWSHCJKVYMYJOMGSBTUVZLGROKZMIRIKLGADNGXHKJMVYIRTNREWKUHDUM"


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


keys = [
    "EFFECTIVEKEY",
    "EFFECTIVE",
    "KEY",
    "EFFECTIVELOWKEY",
    "EFFECTIVEKEYOW",
    "EFFECTIVEKEYTWO",
    "EFFECTIVEKEYNOW",
]
for k in keys:
    print(f"\nKey: {k}")
    # Try fully
    res = vigenere_decrypt(rf2_decoded, k)
    print(f"Full: {res[:60]}...")
    # Try body
    res_b = vigenere_decrypt(rf2_decoded[12:], k)
    print(f"Body: {res_b[:60]}...")

# Check "EFFECTIVE" anagram again.
# ECFTLFVEKYOW
# E:3, C:1, F:2, T:1, L:1, V:1, K:1, Y:1, O:1, W:1.
# EFFECTIVE = E:4, F:2, C:1, T:1, I:1, V:1.
# Missing: E, I.
# Extra: L, K, Y, O, W.
# L, K, Y -> KYL?
# L, O, W -> LOW or OWL.
# KEY? K, E, Y.
# We have K, Y. Need E.
# We are missing E for EFFECTIVE.
# So we need 2 E's (one for EFFECTIVE, one for KEY).
# Source has 3 E's.
# EFFECTIVE KEY needs 4+1 = 5 E's.
# Source has only 3.
# So it CANNOT be "EFFECTIVE KEY".
#
# "EFFECTIVE" needs 4 E's. Source has 3.
# So it CANNOT be "EFFECTIVE".
#
# Let's count again.
# Source: E, C, F, T, L, F, V, E, K, Y, O, W.
# E: 3.
# F: 2.
# C: 1.
# T: 1.
# L: 1.
# V: 1.
# K: 1.
# Y: 1.
# O: 1.
# W: 1.
#
# Maybe "EFFECT"? E:2, F:2, C:1, T:1.
# Remaining: E, L, V, K, Y, O, W.
# "LOVE"? L, O, V, E. (Remaining: K, Y, W).
# "KEY"? K, E (need E), Y. (Need one more E).
# No E left.
#
# Maybe "TWO"? T, W, O.
# Remaining: E:3, F:2, C:1, L:1, V:1, K:1, Y:1.
# "LEVEL"? L, E, V, E, L (Need 2 L's). Only 1 L.
#
# "CYPHER"? C, Y, P, H, E, R. No P, H, R.
#
# "FLOW"? F, L, O, W.
# Rem: E:3, C:1, F:1, T:1, V:1, K:1, Y:1.
# "KEY"? K, E, Y.
# Rem: E:2, C:1, F:1, T:1, V:1.
# "EFFECT"? E:2, F:1 (Need 2 Fs).
#
# What if `ECFTLFVEKYOW` is correct but slightly scrambled?
# What if it's "VE"?
#
# Let's try Vigenere with the STRING ITSELF `ECFTLFVEKYOW` again?
# I did, result was `RHGG...`.
#
# Maybe the INNER cipher is NOT Vigenere?
# "Lattice" could be "Playfair".
# Or "Beaufort".
#
# Let's try BEAUFORT with `ECFTLFVEKYOW`.
# Beaufort: P = K - C.
# If K is `ECFT...` and C is `ECFT...` (prefix), P = 0 ('A').
# So prefix becomes 'A's.
# Body?


def beaufort_decrypt(text, key):
    key = key.upper()
    pt = ""
    key_idx = 0
    for char in text:
        if char in string.ascii_uppercase:
            k_char = ord(key[key_idx % len(key)]) - ord("A")
            c_char = ord(char) - ord("A")
            # P = (K - C) % 26
            p_val = (k_char - c_char) % 26
            pt += chr(p_val + ord("A"))
            key_idx += 1
        else:
            pt += char
    return pt


print("\n--- Beaufort Decrypt with ECFTLFVEKYOW ---")
bf_res = beaufort_decrypt(rf2_decoded[12:], "ECFTLFVEKYOW")
print(f"Result: {bf_res}")

# Try Variant Beaufort: P = C - K? (This is Vigenere Decrypt). I did that.
