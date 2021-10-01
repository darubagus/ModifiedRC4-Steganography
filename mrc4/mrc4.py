"""
    Schema:
        Menggunakan algoritma RC4 dan Feistel:
        1. KSA: Menginisiasi S, yakni array dengan permutasi nilai 0-255
        2. PRGA: ...
        3. Feistel
"""

from citra.Image_Stego import binstr2bin, file2bin, savefile, str2bin


key = None

def acquire_key(input_key):
    global key
    if input_key == None or input_key == "":
        # Default key (soalnya belum nambahin field key buat rc4 sendiri di stego)
        key = "Stego"
        return
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
    message_ints = str_to_ints(message)
    for idx in range(len(message_ints)):
        result += chr(message_ints[idx] ^ keystream[idx%n_keystream])
    return result

def str_to_ints(input_text: str):
    """
        Converts string to list of ints, where each char in string is mapped to its int ASCII value
    """
    return [ord(char) for char in input_text]

def str_to_strbinaries(input_text: str) -> str:
    """
        Converts string to its binary representation
        Example:
        'abcd' --> '01100001011000100110001101100100'
    """
    result = ""
    for char in input_text:
        result += format(ord(char), "08b")
    return "".join(result)

def strbinaries_to_char(content) -> str:
    """
        [DESC]
            Mengkonversi list of str yang merepresentasikan binary ke text/string
        [PARAMS]
            content: list[str]      { list of str. String merupakan binary representation dalam format 1 byte
                                    sehingga len(content) merupakan kelipatan 8 }
    """
    result = ""
    for i in range(len(content)//8):
        byte = content[i*8 : (i+1)*8]
        result += chr(int(byte, 2))
    return result

def cr4_convert_char_to_binstr(content):
    """
        [DESC]
            Mengkonversi str text ke list of str yang merepresentasikan binary setiap char
            Contoh:
            'abcd' --> ['01100001', '01100010', '01100011', 01100100']
        [PARAMS]
            content: str      { text yang ingin diubah ke list of str dalam representasi binary 1 byte }
    """
    result = []
    for char in content:
        result.append(format(ord(char), "08b"))
    return result

def cr4_encrypt_message(message):
    """
        [DESC]
            Menerima message untuk dienkripsi sebelum di-passing kepada algoritma stego image
        [PARAMS]
            message: string yang merepresentasikan binary dari file (e.g. 0010010101...)
        [RETURN]
            Hasil enkripsi message dengan Modified RC4 dalam format yang sama dengan input
    """
    global key
    
    # Convert string of binary representation to string of char
    message_text = strbinaries_to_char(message)
    
    # Encrypt
    enc_message_text = encrypt_text(message_text)

    # Convert string of char to string of binary representation
    enc_message = str_to_strbinaries(enc_message_text)

    return enc_message

def cr4_decrypt_file(filename, extension):
    """
        [DESC]
            Membaca file output hasil ekstraksi steganografi, lalu didekripsi dengan algoritma Modified RC4
            Hasilnya di-write menjadi file dengan nama dan ekstensi yang sama
        [PARAMS]
            filename: str   { nama file output hasil ekstraksi steganografi }
            extension: str  { ekstensi file output hasil ekstraksi steganografi }
    """
    # Read file
    path = "output_decode/" + filename + "." + extension
    content_binstr = file2bin(path)

    # Convert file content into string of char
    content_text = strbinaries_to_char(content_binstr)

    # Decrypt
    content_text = decrypt_text(content_text)

    # Convert string of char to binary
    decr_content = binstr2bin(str2bin(content_text))

    # Write file
    savefile(decr_content, filename, extension)


def feistel(input_message: str, input_key: str, encrypt: bool, num_of_steps: int = 3) -> str:
    """
        [DESC]
            Melakukan enkripsi dengan Feistel Network menggunakan fungsi
            f(S, M) = S ^ M, di mana S adalah subkey dan M adalah message.
            Subkey S ke-i merupakan substring ke-i dari key
            Dilakukan sebanyak num_of_steps (jangan assign nilainya dengan bil. genap, somehow error wkwkw)
        [PARAMS]
            input_message: str  { pesan yang akan dienkripsi }
            input_key: str  { key yang digunakan untuk enkripsi, dalam binary representation }
            num_of_steps: int  { banyak round yang dilakukan }
        [RETURN]
            Hasil enkripsi Feistel
    """
    n_message_part = len(input_message)//2
    n_key = len(input_key)
    if num_of_steps != 0:
        n_key_part = n_key//num_of_steps
    subpart1 = input_message[:n_message_part]
    subpart2 = input_message[n_message_part:]

    if encrypt:
        iterate_key = range(num_of_steps)
    else:
        iterate_key = range(num_of_steps)[::-1]

    for i in iterate_key:
        # get the i-th subkey, i.e. the i-th substring of key
        subkey_i = input_key[i*n_key_part:(i+1)*n_key_part]

        # function f(subkey_i, subpart2)
        # generate keystream for subpart 2, then XOR
        keystream_i = lfsr_txt(subpart2, subkey_i)
        func_result = xor_message(subpart2, keystream_i)

        # XOR the result with subpart1
        xor_result = xor_message(subpart1, str_to_ints(func_result))
        
        subpart1, subpart2 = subpart2, xor_result
        
    subpart1, subpart2 = subpart2, subpart1

    """
    if encrypt:
        for i in range(num_of_steps):
            # get the i-th subkey, i.e. the i-th substring of key
            subkey_i = input_key[i*n_key_part:(i+1)*n_key_part]

            # function f(subkey_i, subpart2)
            # generate keystream for subpart 2, then XOR
            keystream_i = lfsr_txt(subpart2, subkey_i)
            func_result = xor_message(subpart2, keystream_i)

            # XOR the result with subpart1
            xor_result = xor_message(subpart1, str_to_binaries(func_result))
            
            subpart1, subpart2 = subpart2, xor_result
            
        subpart1, subpart2 = subpart2, subpart1
        
    else:
        # subpart1, subpart2 = subpart2, subpart1
        for i in range(num_of_steps)[::-1]:
            # get the i-th subkey, i.e. the i-th substring of key
            subkey_i = input_key[i*n_key_part:(i+1)*n_key_part]

            # function f(subkey_i, subpart2)
            # generate keystream for subpart 2, then XOR
            keystream_i = lfsr_txt(subpart2, subkey_i)
            func_result = xor_message(subpart2, keystream_i)

            # XOR the result with subpart1
            xor_result = xor_message(subpart1, str_to_binaries(func_result))
            
            subpart1, subpart2 = subpart2, xor_result
        
        subpart1, subpart2 = subpart2, subpart1
    """
    
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
    """
        Reads file and return the content (string)
    """
    from pathlib import Path
    # path = Path(__file__).parent / f"../{filename}"
    path = filename
    
    with open(path, "r") as file:
        return file.readlines()

def writefile_txt(filename: str="output.txt", content:str=""):
    """
        Writes content (string) to file
    """
    from pathlib import Path
    # path = Path(__file__).parent / f"../{filename}"
    path = filename

    with open(path, 'wb') as file:
        file.write(content)

def readfile_bin(filename: str = "blue.png"):
    """
        Reads file and return the content (binary)
    """
    from pathlib import Path
    path = filename
    
    with open(path, 'rb') as file:
        temp = []
        byte = file.read(1)
        while byte:
            temp.append(int.from_bytes(byte, "big"))
            byte = file.read(1)
        
        temp = [bin(bits)[2:] for bits in temp]
        result = []
        for e in temp:
            if len(e) < 8:
                e = (8 - len(e)) * "0" + e
            result.append(e)
        
        return "".join([chr(int(e, 2)) for e in result])

def writefile_bin(filename: str="output.png", content: str=""):
    """
        Writes contents (binary) into file
    """
    from pathlib import Path
    # path = Path(__file__).parent / f"../{filename}"
    path = filename
    
    with open(path, 'wb') as file:
        bytes = []
        for char in content:
            byte = int.to_bytes(ord(char), 1, "big")
            bytes.append(byte)
        file.write(b"".join(bytes))

def initializeS(key: str):
    """
        Initializes array S for RC4 algorithm
        S is a permutation of the list containing the numbers 0-255
    """
    key = str_to_strbinaries(key)
    temp = [i for i in range(256)]
    lk = len(key)
    j = 0
    for i in range(256):
        j = (j + temp[i] + int(key[i%lk])) % 256
        temp[i], temp[j] = temp[j], temp[i]
    return temp

def encrypt_text(P: str) -> str:
    """
        [DESC]
            Encrypt a plaintext P with respect to the permutation array S, according to the RC4 algorithm
            Then, the result is encrypted with Feister algorithm
        [PARAMS]
            P: str          { the plaintext to be encrypted }
            S: list[int]    { permutation array }
        [RETURN]
            Ciphertext as the result of RC4 and then Feister
    """
    global key
    S = initializeS(key)
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
    C = feistel(C, str_to_strbinaries(key), encrypt=True)
    return C

def decrypt_text(C: str) -> str:
    """
        [DESC]
            Decrypt the ciphertext with Feister algorithm
            Then, the result is decrypted with respect to the permutation array S, according to the RC4 algorithm
        [PARAMS]
            C: str          { the ciphertext to be decrypted }
            S: list[int]    { permutation array }
        [RETURN]
            Plaintext as the result of Feister and then RC4
    """
    global key
    S = initializeS(key)
    # Feistel here
    C = feistel(C, str_to_strbinaries(key), encrypt=False)

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
            while key == None:
                key = input("Input key: \n>>> ")
            acquire_key(key)
            ciphertext = encrypt_text(message)
            print("The encrypted message is:\n>>>", ciphertext, "<<<")
            key = None

            while key == None:
                key = input("Input key: \n>>> ")
            acquire_key(key)
            plaintext = decrypt_text(ciphertext)
            print("The decrypted message is:\n>>>", plaintext, "<<<")
            key = None

            print("- - - - - - - - - - - - - - - - - - - - ")
    elif (mode == "2"):
        message = readfile_bin()
        print("The message is:\n>>>", message, "<<<")
        while True:
            while key == None:
                key = input("Input key: \n>>> ")
            acquire_key(key)
            ciphertext = encrypt_text(message)
            print("The encrypted message is:\n>>>", ciphertext, "<<<")
            key = None
            writefile_bin(filename="output.png", content=ciphertext)

            while key == None:
                key = input("Input key: \n>>> ")
            acquire_key(key)
            plaintext = decrypt_text(ciphertext)
            print("The decrypted message is:\n>>>", plaintext, "<<<")
            key = None
            writefile_bin(filename="output.png", content=plaintext)

            print("- - - - - - - - - - - - - - - - - - - - ")

if __name__ == "__main__":
    main()
    # print(readfile_bin())