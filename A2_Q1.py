# Group: DAN/EXT 28
# Members: Hendrick Dang – S395598, Mehraab Ferdouse – S393148,
#          Fateen Rahman – S387983, Kevin Zhu – S387035

# per-run mapping by encrypted occurrence → original char
enc_map = {}
enc_counts = {}
dec_counts = {}

def enc_char(ch, s1, s2):
    if 'a' <= ch <= 'z':
        if ch <= 'm':
            return chr((ord(ch) - 97 + (s1 * s2)) % 26 + 97)
        else:
            return chr((ord(ch) - 97 - (s1 + s2)) % 26 + 97)
    elif 'A' <= ch <= 'Z':
        if ch <= 'M':
            return chr((ord(ch) - 65 - s1) % 26 + 65)
        else:
            return chr((ord(ch) - 65 + (s2 * s2)) % 26 + 65)
    else:
        return ch  # keep spaces, digits, symbols

def encrypt_text(text, s1, s2):
    out = []
    for ch in text:
        e = enc_char(ch, s1, s2)
        c = enc_counts.get(e, 0) + 1
        enc_counts[e] = c
        enc_map[f"{e}{c}"] = ch
        out.append(e)
    return "".join(out)

def decrypt_text(text):
    out = []
    for ch in text:
        c = dec_counts.get(ch, 0) + 1
        dec_counts[ch] = c
        out.append(enc_map.get(f"{ch}{c}", ch))
    return "".join(out)

def norm(s):
    return s.replace("\r\n", "\n").rstrip("\n")

# --- main ---
s1 = int(input("Enter Shift1: "))
s2 = int(input("Enter Shift2: "))

raw = open("raw_text.txt", "r", encoding="utf-8").read()
enc = encrypt_text(raw, s1, s2)
open("encrypted_text.txt", "w", encoding="utf-8", newline="").write(enc)

dec = decrypt_text(enc)
open("decrypted_text.txt", "w", encoding="utf-8", newline="").write(dec)

print("Successful" if norm(raw) == norm(dec) else "Unsuccessful")
