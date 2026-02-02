import itertools

words = [
    "password", "admin", "12345678", "1234567890", "qwerty",
    "ctf", "challenge", "CTF_Challenge", "CTF-Challenge",
    "plant", "factory", "bridge", "sky", "air", "kutyu", "net", "boei",
    "wifi", "wlan", "access", "point", "ap",
    "accton", "test", "guest", "user"
]

variations = []
for w in words:
    variations.append(w)
    variations.append(w.lower())
    variations.append(w.upper())
    variations.append(w.capitalize())

suffixes = ["", "1", "12", "123", "1234", "12345", "!", "2024", "2025", "2026", "_2025", "_2024"]

final_list = set()
for v in variations:
    for s in suffixes:
        final_list.add(v + s)

# specific likely ones found in other CTFs or generic
final_list.add("mysimplepassword")
final_list.add("aircrack")
final_list.add("aircrack-ng")

with open("wordlist_gen.txt", "w") as f:
    for p in final_list:
        if len(p) >= 8: # WPA minimum length
            f.write(p + "\n")
