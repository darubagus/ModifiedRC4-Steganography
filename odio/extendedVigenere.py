
def mod(n,m):
    return (((n%m)+m) % m)

def _encrypt(text, key):
    cipher = ''
    for i in range(len(text)):
        c = ord(text[i])
        k = ord(key[mod(i,len(key))])
        cipher += chr(mod((c-k), 256))
    
    return cipher

def _decrypt(input, key):
    text = ''
    for i in range (len(input)):
        c = ord(input[i])
        k = ord(key[mod(i,len(key))])
        text += chr(mod(c - k, 256))
    return text

