import subprocess
import itertools

ssid = "CTF_Challenge"

base_words = [
    "password",
    "12345678",
    "admin",
    "root",
    "guest",
    "user",
    "Plant",
    "plant",
    "Factory",
    "factory",
    "CTF",
    "ctf",
    "Challenge",
    "challenge",
    "CTF_Challenge",
    "ctf_challenge",
    "Net-Kutyu",
    "net-kutyu",
    "netkutyu",
    "NetKutyu",
    "Boei",
    "boei",
    "Bridge",
    "bridge",
    "Air",
    "air",
    "Sky",
    "sky",
    "Accton",
    "accton",
    "cheetah",
    "smc",
    "edgecore",
    "welcome",
    "Welcome",
    "welc0me",
    "password123",
    "123456",
    "5cdb6a8b",
    "5cdb6a8b0cd45ec27730b0b4a6f178f63baef687",
    "safety",
    "Safety",
    "first",
    "First",
    "SafetyFirst",
    "robot",
    "machine",
    "iot",
    "scada",
    "cisco",
    "linksys",
    "airlive",
    "dlink",
    "huawei",
    "tplink",
    "ubiquiti",
    "flag",
    "Flag",
    "FLAG",
    "pass",
    "security",
    "wifi",
    "wlan",
]

# Generate variations
passwords = set(base_words)

# Add variations with numbers
for w in base_words:
    passwords.add(w + "1")
    passwords.add(w + "123")
    passwords.add(w + "!")
    passwords.add(w + "2024")
    passwords.add(w + "2025")
    passwords.add(w + "2026")

# Add lowercase
for w in base_words:
    passwords.add(w.lower())
    passwords.add(w.upper())
    passwords.add(w.capitalize())

passwords_list = list(passwords)
print(f"Brute forcing with {len(passwords_list)} passwords...")


def try_crack(password):
    # Use -o wlan.enable_decryption:TRUE -o uat:80211_keys:"wpa-pwd","password:SSID"
    # We check if we can see any IP packets.
    # Note: If decryption works, we usually see TCP/UDP/IP/ARP etc.
    # If decryption fails, we see only IEEE 802.11 Data (encrypted).

    cmd = [
        "tshark",
        "-r",
        "Plant.cap",
        "-o",
        "wlan.enable_decryption:TRUE",
        "-o",
        f'uat:80211_keys:"wpa-pwd","{password}:{ssid}"',
        "-Y",
        "ip",
        "-c",
        "1",
    ]
    try:
        # Timeout quickly as successful decryption allows almost instant match with -c 1
        # However, tshark startup takes time. 2 seconds is enough for startup + check.
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        if result.returncode == 0 and len(result.stdout) > 0:
            return True
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        print(f"Error with {password}: {e}")
    return False


# Try in chunks or just loop
found = False
for i, p in enumerate(passwords_list):
    if i % 10 == 0:
        print(f"Checking {i}/{len(passwords_list)}: {p}")
    if try_crack(p):
        print(f"\n[+] SUCCESS! Password found: '{p}'")
        found = True
        break

if not found:
    print("\n[-] Password not found.")
