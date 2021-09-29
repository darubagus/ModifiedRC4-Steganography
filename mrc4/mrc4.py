"""
    Schema:
        Menggunakan algoritma RC4:
        1. KSA: Menginisiasi S, yakni array dengan permutasi nilai 0-255
        2. PRGA: ...
        3. Feistel (DES)
"""

key = None

def acquire_key(input_key):
    global key
    key = input_key
    # while key == None:
    #     key = input("Input key: \n>>> ")
    
    # convert key to binary
    # key = "".join(str_to_strbinaries(key))

def xor_message(message: str, keystream) -> str:
    """
        [DESC]
            menglakukan XOR antara message (string) dengan keystream list of integer 0-255
    """
    result = ""
    n_keystream = len(keystream)
    message_ints = str_to_binaries(message)
    for idx in range(len(message_ints)):
        result += chr(message_ints[idx] ^ keystream[idx%n_keystream])
    return result

def str_to_binaries(input_text: str) :
    return [ord(char) for char in input_text]

def str_to_strbinaries(input_text: str) :
    temp = [bin(bits)[2:] for bits in [ord(char) for char in input_text]]
    result = []
    for e in temp:
        if len(e) < 8:
            e = (8 - len(e)) * "0" + e
        result.append(e)
    return "".join(result)


def feistel(input_message: str, input_key: str, encrypt: bool, num_of_steps: int = 3) -> str:
    """
        [DESC]
            Melakukan enkripsi dengan Feistel Network menggunakan fungsi
            f(S, M) = S ^ M, di mana S adalah subkey dan M adalah message.
            Dilakukan sebanyak num_of_steps
        [PARAMS]
            input_message: str  { pesan yang akan dienkripsi }
            input_key: str  { key yang digunakan untuk enkripsi, dalam binary representation }
            num_of_steps: int  { banyak round yang dilakukan }
        [RETURN]
            Hasil enkripsi
    """
    n_message_part = len(input_message)//2
    n_key = len(input_key)
    if num_of_steps != 0:
        n_key_part = n_key//num_of_steps
    subpart1 = input_message[:n_message_part]
    subpart2 = input_message[n_message_part:]

    if encrypt:
        for i in range(num_of_steps):
            subkey_i = input_key[i*n_key_part:(i+1)*n_key_part]
            keystream_i = lfsr_txt(subpart2, subkey_i)
            func_result = xor_message(subpart2, keystream_i)
            xor_result = xor_message(subpart1, str_to_binaries(func_result))
            
            subpart1, subpart2 = subpart2, xor_result
    else:
        for i in range(num_of_steps)[::-1]:
            subkey_i = input_key[i*n_key_part:(i+1)*n_key_part]
            keystream_i = lfsr_txt(subpart2, subkey_i)
            func_result = xor_message(subpart2, keystream_i)
            xor_result = xor_message(subpart1, str_to_binaries(func_result))
            
            subpart1, subpart2 = subpart2, xor_result
    
    subpart1, subpart2 = subpart2, subpart1

    return subpart1 + subpart2

def lfsr_txt(input_message: str, subkey: str):
    """
        [DESC]
            Berdasarkan algoritma Linear Shift register Key:
            menghasilkan keystream yang dibutuhkan untuk mengenkripsi input_message
        [PARAMS]
            input_message: str  { dalam bentuk ASCII representation }
            subkey: str { dalam bentuk binary representation }
        [RETURN]
            keystream yang siap di-XOR-kan untuk mengenkripsi input_message
    """
    def xor_bits(bits):
        result = 0
        for bit in bits:
            result ^= bit
        return result
    
    n_input_message = len(input_message)
    register = [1 if bit == "1" else 0 for bit in subkey]
    
    keystream = []
    i = 0
    while i < n_input_message:
        temp = "0b"
        for _ in range(8):
            register.append(xor_bits(register))
            temp += str(register.pop(0))
        keystream.append(int(temp, 2))
        i += 1
    return keystream


def readfile_txt(filename: str = "plaintext.txt"):
    from pathlib import Path
    # path = Path(__file__).parent / f"../{filename}"
    path = filename
    
    with open(path, "r") as file:
        return file.readlines()

def writefile_txt(filename: str="output.txt", content:str=""):
    from pathlib import Path
    # path = Path(__file__).parent / f"../{filename}"
    path = filename

    with open(path, 'wb') as file:
        file.write(content)

def readfile_bin(filename: str = "blue.png"):
    from pathlib import Path
    path = filename
    
    with open(path, 'rb') as file:
        temp = []
        while (byte := file.read(1)):
            temp.append(int.from_bytes(byte, "big"))
        
        temp = [bin(bits)[2:] for bits in temp]
        result = []
        for e in temp:
            if len(e) < 8:
                e = (8 - len(e)) * "0" + e
            result.append(e)
        
        return "".join([chr(int(e, 2)) for e in result])

def writefile_bin(filename: str="output.png", content: str=""):
    from pathlib import Path
    # path = Path(__file__).parent / f"../{filename}"
    path = filename
    
    with open(path, 'wb') as file:
        bytes = []
        for char in content:
            byte = int.to_bytes(ord(char), 1, "big")
            bytes.append(byte)
        file.write(b"".join(bytes))

def initializeS():
    global key
    key = str_to_strbinaries(key)
    temp = [i for i in range(256)]
    lk = len(key)
    j = 0
    for i in range(256):
        j = (j + temp[i] + int(key[i%lk])) % 256
        temp[i], temp[j] = temp[j], temp[i]
    return temp

def encrypt_text(P: str) -> str:
    S = initializeS()
    i = j = 0
    C = ""
    for idx in range(len(P)):
        i = (i + 1) % 256      # increase i
        j = (j + S[i]) % 256   # j is random
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t]         # keystream byte
        c_bytes = u ^ ord(P[idx])   # ciphertext byte
        C += chr(c_bytes)
    
    # Feistel here
    global key
    C = feistel(C, str_to_strbinaries(key), True)
    return C

def decrypt_text(C: str) -> str:
    S = initializeS()
    # Feistel here
    global key
    C = feistel(C, str_to_strbinaries(key), False)

    i = j = 0
    P = ""
    for idx in range(len(C)):
        i = (i + 1) % 256      # increase i
        j = (j + S[i]) % 256   # j is random
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        u = S[t]         # keystream byte
        p_bytes = u ^ ord(C[idx])   # ciphertext byte
        P += chr(p_bytes)

    return P

def main():
    global key

    print("Input mode:")
    print("1. Text")
    print("2. Binary")
    mode = input(">>> ")

    if mode == "1":
        message = "Decryption Process \
            The process of decryption in Feistel cipher is almost similar. Instead of starting with a block of plaintext, the ciphertext block is fed into the start of the Feistel structure and then the process thereafter is exactly the same as described in the given illustration. \
            The process is said to be almost similar and not exactly same. In the case of decryption, the only difference is that the subkeys used in encryption are used in the reverse order. \
            The final swapping of ‘L’ and ‘R’ in last step of the Feistel Cipher is essential. If these are not swapped then the resulting ciphertext could not be decrypted using the same algorithm."
        print("The message is:\n>>>", message, "<<<")
        while True:
            acquire_key()
            S = initializeS(key)
            ciphertext = encrypt_text(message, S)
            print("The encrypted message is:\n>>>", ciphertext, "<<<")
            key = None

            acquire_key()
            S = initializeS(key)
            plaintext = decrypt_text(ciphertext, S)
            print("The decrypted message is:\n>>>", plaintext, "<<<")
            key = None

            print("- - - - - - - - - - - - - - - - - - - - ")
    elif (mode == "2"):
        message = readfile_bin()
        print("The message is:\n>>>", message, "<<<")
        while True:
            acquire_key()
            S = initializeS(key)
            ciphertext = encrypt_text(message, S)
            print("The encrypted message is:\n>>>", ciphertext, "<<<")
            key = None
            writefile_bin(filename="output.png", content=ciphertext)

            acquire_key()
            S = initializeS(key)
            plaintext = decrypt_text(ciphertext, S)
            print("The decrypted message is:\n>>>", plaintext, "<<<")
            key = None
            writefile_bin(filename="output.png", content=plaintext)

            print("- - - - - - - - - - - - - - - - - - - - ")

if __name__ == "__main__":
    main()
    # print(readfile_bin())