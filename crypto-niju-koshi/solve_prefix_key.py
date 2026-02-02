# The prefix `ECFTLFVEKYOW` decrypted with `ECFTLFVEKYOW` yields `AAAAAAAAAAAA`.
# This means the prefix IS the key encrypted with ITSELF (or Plaintext 'A'*12 encrypted with Key).
# Usually: C = P + K. If P='A' (0), then C = K.
# So `ECFTLFVEKYOW` *IS* the key stream.
# Since it repeats or is used for the text...
# "Decrypting the outer cipher reveals the key for the inner cipher".
# So the Key IS `ECFTLFVEKYOW`.
#
# But I tried decrypting the whole text with `ECFTLFVEKYOW` and got:
# `AAAAAAAAAAAA RHGGYBUSCMIEMAZAFPSAXFUXFOMOIDYDBWUOAZOBRNMDBDFB...`
#
# Is `RHGGYBUS...` the flag?
# It doesn't look like English.
#
# Wait, if `ECFTLFVEKYOW` is the Key, and Text starts with Key...
# Then Plaintext starts with 'A's?
# Maybe the "Key" is meant to be used for the REST of the message?
# I tried that (`rf2_rest` with `EFFECTIVE`).
# I should try `rf2_rest` with `ECFTLFVEKYOW`.

import string

rf2_decoded = "ECFTLFVEKYOWVJLZJGPWMKWAQCETQUNEHDITJQRHTITHLUIKEBTUCSHHLBTXWRCYJENRWESZEXFHBYTCWSHCJKVYMYJOMGSBTUVZLGROKZMIRIKLGADNGXHKJMVYIRTNREWKUHDUM"
key = "ECFTLFVEKYOW"
rf2_rest = rf2_decoded[12:]


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


decoded = vigenere_decrypt(rf2_rest, key)
print(f"Key: {key}")
print(f"Decoded Body: {decoded}")


# Also check ROT47 of the decoded body?
# ROT47 on English chars usually makes them symbols.
# Maybe ROT13?
def rot13(text):
    res = ""
    for c in text:
        if c in string.ascii_uppercase:
            res += chr((ord(c) - ord("A") + 13) % 26 + ord("A"))
        else:
            res += c
    return res


print(f"ROT13 of body: {rot13(decoded)}")
