# Group: DAN/EXT 28
# Members: Hendrick Dang – S395598, Mehraab Ferdouse – S393148,
#          Fateen Rahman – S387983, Kevin Zhu – S387035

def encrypt(text, s1, s2):
    result = ""
    for ch in text:
        if ch.islower():
            if ch <= 'm':
                result = result + chr((ord(ch) - 97 + (s1 * s2)) % 26 + 97)
            else:
                result = result + chr((ord(ch) - 97 - (s1 + s2)) % 26 + 97)
        elif ch.isupper():
            if ch <= 'M':
                result = result + chr((ord(ch) - 65 - s1) % 26 + 65)
            else:
                result = result + chr((ord(ch) - 65 + (s2 * s2)) % 26 + 65)
        else:
            result = result + ch
    return result

def decrypt(text, s1, s2):
    result = ""
    for ch in text:
        if ch.islower():
            if ch <= 'm':
                result = result + chr((ord(ch) - 97 - (s1 * s2)) % 26 + 97)
            else:
                result = result + chr((ord(ch) - 97 + (s1 + s2)) % 26 + 97)
        elif ch.isupper():
            if ch <= 'M':
                result = result + chr((ord(ch) - 65 + s1) % 26 + 65)
            else:
                result = result + chr((ord(ch) - 65 - (s2 * s2)) % 26 + 65)
        else:
            result = result + ch
    return result

s1 = int(input("Enter Shift1: "))
s2 = int(input("Enter Shift2: "))

raw = open("raw_text.txt").read()
enc = encrypt(raw, s1, s2)
open("encrypted_text.txt", "w").write(enc)

dec = decrypt(enc, s1, s2)
open("decrypted_text.txt", "w").write(dec)

# Simple compare (ignoring trailing newlines)
if raw.strip() == dec.strip():
    print("Successful")
else:
    print("Unsuccessful")
