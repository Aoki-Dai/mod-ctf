import hashlib
import binascii
import hmac
import sys

# Inputs
ssid = "CTF_Challenge"
ap_mac_str = "0000e86e6e5a"
sta_mac_str = "1ebc130cfaf0"
anonce_str = "ab3c88a17a44f6912f17f44e7b4191ff0bff203c651a9c73ba9f3caa6c9fbedf"
snonce_str = "ecf0158b1c8ccfce384a2b1317224ce5cf1235e2eb9146a6d217f1019b99b35c"
mic_expected_str = "f5157d2c0ce641b686cb799ca4554b39"

eapol_hex = "0203007502010a00100000000000000001ecf0158b1c8ccfce384a2b1317224ce5cf1235e2eb9146a6d217f1019b99b35c0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f5157d2c0ce641b686cb799ca4554b39001630140100000fac040100000fac040100000fac020c00"

# Convert to bytes
ap_mac = binascii.unhexlify(ap_mac_str)
sta_mac = binascii.unhexlify(sta_mac_str)
anonce = binascii.unhexlify(anonce_str)
snonce = binascii.unhexlify(snonce_str)
mic_expected = binascii.unhexlify(mic_expected_str)
eapol_data = bytearray(binascii.unhexlify(eapol_hex))

# Zero out the MIC in EAPOL data for calculation
eapol_data[81 : 81 + 16] = b"\x00" * 16


def custom_prf512(key, A, B):
    R = b""
    A_bytes = A.encode()
    for i in range(4):
        msg = A_bytes + b"\x00" + B + bytes([i])
        R += hmac.new(key, msg, hashlib.sha1).digest()
    return R[:64]


def check_password(password):
    if len(password) < 8 or len(password) > 63:
        return False

    pmk = hashlib.pbkdf2_hmac("sha1", password.encode(), ssid.encode(), 4096, 32)

    if ap_mac < sta_mac:
        addrs = ap_mac + sta_mac
    else:
        addrs = sta_mac + ap_mac

    if anonce < snonce:
        nonces = anonce + snonce
    else:
        nonces = snonce + anonce

    data = addrs + nonces

    ptk = custom_prf512(pmk, "Pairwise key expansion", data)
    kck = ptk[0:16]
    mic_calc = hmac.new(kck, eapol_data, hashlib.sha1).digest()[:16]

    return mic_calc == mic_expected


# Generate wordlist
words = [
    "Plant",
    "Factory",
    "Air",
    "Sky",
    "Bridge",
    "Net",
    "Kutyu",
    "Rainbow",
    "Cloud",
    "Connect",
    "Link",
    "Smart",
    "Safe",
    "Safety",
    "Admin",
    "Pass",
    "User",
    "Guest",
    "Ctf",
    "Challenge",
    "Flag",
    "Test",
    "Wlan",
    "Wifi",
    "Accton",
    "Cisco",
    "Root",
    "Yamada",
    "Suzuki",
    "Tanaka",
    "Sato",
    "Takahashi",
    "Koba",
    "Kojo",
    "Anzen",
    "Daiichi",
    "Yoshi",
    "Ok",
    "Good",
    "Welcome",
    "Hello",
    "World",
    "Kuchu",
    "Kakehashi",
    "Sora",
    "Tenku",
    "Netkutyu",
    "NetKutyu",
]

candidates = set()
candidates.add("password")
candidates.add("12345678")
candidates.add("123456789")
candidates.add("1234567890")
candidates.add("00000000")
candidates.add("11111111")
candidates.add("CTN_Challenge")
candidates.add("CTF_Challenge")
candidates.add("CTF-Challenge")
candidates.add("CTFChallenge")
candidates.add("CtfChallenge")

suffixes = [
    "",
    "1",
    "12",
    "123",
    "1234",
    "12345",
    "123456",
    "!",
    "?",
    ".",
    "_",
    "@",
    "2024",
    "2025",
    "2026",
    "2020",
    "2019",
    "01",
    "001",
]

for w1 in words:
    forms1 = {w1, w1.lower(), w1.upper()}
    for f1 in forms1:
        for s in suffixes:
            candidates.add(f1 + s)

        # Combine with another word
        for w2 in words:
            forms2 = {w2, w2.lower()}
            for f2 in forms2:
                candidates.add(f1 + f2)
                candidates.add(f1 + "_" + f2)
                candidates.add(f1 + "-" + f2)
                candidates.add(f1 + "." + f2)
                candidates.add(f1 + f2 + "1")
                candidates.add(f1 + f2 + "123")
                candidates.add(f1 + f2 + "!")
                candidates.add(f1 + "_" + f2 + "!")

print(f"Testing {len(candidates)} passwords...")

for i, p in enumerate(candidates):
    if i % 5000 == 0:
        print(f"Checking {i}: {p}")
        sys.stdout.flush()
    if check_password(p):
        print(f"\n[+] SUCCESS! Password found: '{p}'")
        break
else:
    print("\n[-] Password not found.")
