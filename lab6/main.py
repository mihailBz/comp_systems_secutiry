def KSA(key):
    S = list(range(256))

    j = 0
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]
    return S


def PRGA(S, data):
    out = []
    j = 0
    i = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(
            ord(char) ^ S[(S[i] + S[j]) % 256]
        )
    return out

def d_PRGA(S, data):
    out = []
    j = 0
    i = 0
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(
            char ^ S[(S[i] + S[j]) % 256]
        )
    return out


def main():
    msg = 'hello this is test message'
    key = 'mykey'

    b_msg = msg.encode()
    b_key = key.encode()

    S = KSA(key)
    print([hex(ord(i)) for i in msg])
    encrypted_msg = PRGA(S, msg)
    S = KSA(key)
    print([hex(i) for i in encrypted_msg])
    print([hex(i) for i in d_PRGA(S, encrypted_msg)])

if __name__ == '__main__':
    main()
