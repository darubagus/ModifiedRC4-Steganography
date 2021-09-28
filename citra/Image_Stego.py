import struct
import numpy as np
from PIL import Image

#---------------------------UTILITIES----------------------------

#String to Binary String
def str2bin(text):
    if type(text) == str:
        return ''.join(format(ord(i), '08b') for i in text)
    return 

#File to Binary String
def file2bin(path):
    file = open(path, 'rb')
    content = file.read()
    file.close()
    return ''.join([format(i, "08b") for i in content])

#Save File
def savefile(content, filename, ext):
    path = filename + "." + ext
    file = open(path, 'wb')
    file.write(content)
    file.close 

#Binary String to Binary
def binstr2bin(binstr):
    in_bytes = bytes('', 'utf-8')
    split8 = [binstr[i:i+8] for i in range(0, len(binstr), 8)]
    for byte in split8:
        in_bytes += struct.pack('B', int(byte, 2))
    return in_bytes

def addDelim(msg):
    delim = str2bin("!@#$%")
    return msg + delim

def imgSize(img):
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB': n = 3
    elif img.mode == 'RGBA': n = 4   

    total_pixels = array.size//n
    return (total_pixels, n)

def generatePxOrder(imgSize, random, *s):
    if (random): 
        if s == (): s = [0]
        return np.random.RandomState(seed=s[0]).permutation(imgSize).tolist()
    return [i for i in range(imgSize)]
    
#---------------------------ENCODING----------------------------
def encode(message, srcFile, destFile, random, *s):
    img = Image.open(srcFile, 'r')
    width, height = img.size
    size = imgSize(img)[0]
    n = imgSize(img)[1]
    array = np.array(list(img.getdata()))

    message = addDelim(message)

    #Check
    msgSize = len(message)
    if msgSize > size:
        print("Bigger image or smaller message required")
        return 
    
    #Encode
    i = 0
    order = generatePxOrder(size, random, s)

    for a in order:
        for b in range(0, 3):
            if i < msgSize:
                array[a][b] = int(bin(array[a][b])[2:9] + message[i], 2)
                i += 1

    array=array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(destFile)
    print("Image Encoded Successfully")

#Run Encoding
def startEncode():
    srcFile = input("Masukkan path menuju file pembungkus: ")
    mode = int(input("Mau masukin file atau ketik pesan untuk disembunyikan? \n 1.File \n 2.Ketik\n"))

    if mode == 1: 
        path = input("Masukkan path ke file: ")
        message = file2bin(path)
    else:
        msg = input("Masukkan pesan: ")
        message = str2bin(msg)

    random = input("Random or not bro? (Yes/No): ")
    destFile = input("Masukkan path untuk file hasil: ")

    if random == "Yes": 
        seed = int(input("Masukkan stego-key!: "))
        encode(message, srcFile, destFile, True, seed)
    else: 
        encode(message, srcFile, destFile, False)
        
#---------------------------DECODING----------------------------
def decode(srcFile, destFile, fileFormat, random, *s):

    img = Image.open(srcFile, 'r')
    size = imgSize(img)[0]
    array = np.array(list(img.getdata()))

    decoded_bits = ''

    order = generatePxOrder(size, random, s)
    for p in order:
        for q in range(0, 3):
            decoded_bits += (bin(array[p][q])[2:][-1])
    print(decoded_bits[-40:])
    decoded_bits = [decoded_bits[i:i+8] for i in range(0, len(decoded_bits), 8)]

    #Cracking the message
    messageChar = ""
    for i in range(len(decoded_bits)):
        if messageChar[-5:] == "!@#$%":
            break
        else:
            messageChar += chr(int(decoded_bits[i], 2))

    if "!@#$%" in messageChar:
        noDelim = messageChar[:-5]
        if fileFormat == "txt":
            print("Hidden Message:", noDelim)
        msgbin = binstr2bin(str2bin(noDelim))
        print(decoded_bits[:-5])
        savefile(msgbin, destFile, fileFormat)

    else:
        print("No Hidden Message Found")


def startDecode():
    srcFile = input("Masukkan path menuju file pembungkus: ")

    random = input("Random or not bro? (Yes/No): ")
    destFile = input("Masukkan nama untuk file hasil: ")
    destFormat = input("Masukkan format untuk file hasil: ")

    if random == "Yes": 
        seed = int(input("Masukkan stego-key!: "))
        decode(srcFile, destFile, destFormat, True, seed)
    else: 
        decode(srcFile, destFile, destFormat, False)


#TESTING
startEncode()
startDecode()
