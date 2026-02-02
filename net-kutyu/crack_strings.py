import hashlib
import binascii
import hmac
import subprocess

# Inputs (Same as before)
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
    # Only ascii
    try:
        password.encode("ascii")
    except:
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


print("Extracting strings from Plant.cap...")
try:
    output = subprocess.check_output(["strings", "Plant.cap"], text=True)
    lines = output.splitlines()
    candidates = set()
    for line in lines:
        s = line.strip()
        if len(s) >= 8 and len(s) <= 63:
            candidates.add(s)

    print(f"Testing {len(candidates)} strings from file...")
    for p in candidates:
        if check_password(p):
            print(f"FOUND: {p}")
            break
    else:
        print("Not found in strings.")
except Exception as e:
    print(f"Error: {e}")
