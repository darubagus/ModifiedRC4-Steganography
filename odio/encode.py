import wave
import os
import random
import base64

# FIle thingy
def get_extension(path):
    has_extention = path.split("/")[-1].find(".") != -1
    extension = ""

    if (has_extention):
        extension = path.split(".")[-1]

    return extension

def readFiles(path):
    with open(path, 'rb') as f:
        byte_file = f.read()

    return byte_file

def writeFiles(path, byteFiles):
    with open(path, 'wb') as f:
        f.write(byteFiles)

def readAudioFile(audiopath):
    audio = wave.open(audiopath, "rb")
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    return frames

def getAudioMetadata(audiopath):
    audio = wave.open(audiopath, 'rb')
    metadata = audio.getparams()
    audio.close()

    return metadata

def initBuffAudio(audiopath):
    audio = wave.open(audiopath, 'rb')
    initBuff = audio.readframes(-1)
    initBuff = [item + 0 for item in initBuff]
    audio.close()

    return initBuff

def writeAudioFile(audiopath, frames, metadata):
    audio = wave.open(audiopath, 'wb')
    audio.setparams(metadata)
    audio.writeframes(frames)
    audio.close()


def decimal2Binary(number):
    return bin(number).replace("0b","")

def countSeed(Key):
    # stegoKey = input("Masukkan stegokey")
    return sum([ord(i) for i in range(Key)])

def frameRandomizer(frames, randomizeFrame, seed, frame_list):
    if randomizeFrame:
        sign = 1
    else:
        sign = 0
    
    frames[1] = frames[1] & 254 | sign
    if randomizeFrame:
        random.seed(seed)
        random.shuffle(frame_list)
    
    return frame_list

def modifyFrame(arrayBit, frames, frame_list):
    idx = 0
    for i in (frame_list):
        if idx >= len(arrayBit):
            break
        if i >= 2:
            frames[i] = frames[i] & 254 | arrayBit[idx]
            idx += 1
    
    return frames

def encrypt_message(frames, encrypted, string_message, *key):
    if encrypted:
        sign = 1
    else:
        sign = 0

    frames[0] = frames[0] & 254 | sign

    # if encrypted:   # ini nanti pake RC4
    #     # return string_message = ''
    
    return string_message

def encode(nottypedMessage, message, src, dest, random=False, encrypted=False, *s):
    audio = readAudioFile(src)
    metadata = getAudioMetadata(src)
    initBuff = initBuffAudio(src)
    stringMessage = str(message)
    if (nottypedMessage):
        msg = get_extension(message)

        byteMessage = readFiles(message)
        message = base64.b64encode(byteMessage).decode('utf-8')

        lenMsg = str(len(message)+len(msg)+2)
        stringMessage = lenMsg+'#'+msg+'#'+message

    if encrypted:
        encryptedMsg = encrypt_message(audio, encrypted, stringMessage, s)
    else:
        encryptedMsg = encrypt_message(audio, encrypted, stringMessage)

    if 0.9*len(audio)//8 < len(stringMessage):
        print("Message is larger than payload capacity")
    
    bits = map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in stringMessage]))
    arrayBit = list(bits)

    frameList = list(range(len(audio)))
    randFrame = frameRandomizer(audio, random, s, frameList)
    modFrame = modifyFrame(arrayBit,audio, frameList)

    return bytes(audio), metadata

def main():
    # srcFile = input("Masukkan path menuju file pembungkus: ")
    # mode = int(input("Mau masukin file atau ketik pesan untuk disembunyikan? \n 1.File \n 2.Ketik\n"))
    srcFile = "original/contho.wav"
    mode = 1
    

    if mode == 1: 
        # path = input("Masukkan path ke file: ")
        path = 'msg/msg.txt'
        message = readFiles(path)
        typedMessage = False
    else:
        msg = input("Masukkan pesan: ")
        message = decimal2Binary(msg)
        typedMessage=True

    # random = input("Random or not bro? (Yes/No): ")
    # destFile = input("Masukkan path untuk file hasil: ")
    random = "Yes"
    destFile = 'stego/hasil1.wav'
    if random == "Yes": 
        seed = input("Masukkan stego-key!: ")
        # encode(message, srcFile, destFile, True, seed)
        hasil,metadata = encode(typedMessage, message, srcFile, destFile, True, False, seed)
        writeAudioFile(destFile, hasil, metadata)
    else: 
        # encode(message, srcFile, destFile, False)
        hasil,  metadata = encode(typedMessage, message, srcFile, destFile, False, False)
        writeAudioFile(destFile, hasil, metadata)
    
if __name__ == "__main__":
    main()