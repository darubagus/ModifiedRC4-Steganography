from base64 import encode
from encodeOO import EncodeAudio
from decodeOO import DecodeAudio
from ioFile import File


def EncodeStart():
    
    # srcFile = input("Masukkan path menuju file pembungkus: ")
    # mode = int(input("Mau masukin file atau ketik pesan untuk disembunyikan? \n 1.File \n 2.Ketik\n"))
    srcFile = "original/contho.wav"
    mode = 1
    
    if mode == 1: 
        # path = input("Masukkan path ke file: ")
        path = 'msg/msg.txt'
        typedMessage = False
    else:
        msg = input("Masukkan pesan: ")
        path = 'msg/' + input("masukkan nama file: ") + '.txt'
        msgFile = File(path)
        msgFile.writeTextFile(msg)
        typedMessage=True

    # random = input("Random or not bro? (Yes/No): ")
    # destFile = input("Masukkan path untuk file hasil: ")
    random = "Yes"
    if random == "Yes": 
        seed = input("Masukkan stego-key!: ")
        encode = EncodeAudio(srcFile, path, seed)

        modifiedFrames = encode.encodeAudio(True, False)

        outputFile = 'stego/' + input('nama file output:') + '.wav'
        output = File(outputFile)
        output.writeAudioFile(modifiedFrames, encode.metadata)
    else:
        seed = ''
        encode = EncodeAudio(srcFile,path, seed)

        modifiedFrames = encode.encodeAudio(False,False)

        outputFile = 'stego/' + input('nama file output:') + '.wav'
        output = File(outputFile)
        output.writeAudioFile(modifiedFrames, encode.metadata)

def DecodeStart():
    # srcFile = input("Masukkan path menuju file pembungkus: ")
    srcFile = 'stego/ninuninu.wav'

    # random = input("Random or not bro? (Yes/No): ")
    random = 'Yes'
    # destFile = input("Masukkan nama untuk file hasil: ")
    # destFormat = input("Masukkan format untuk file hasil: ")

    if random == "Yes": 
        seed = input("Masukkan stego-key!: ")
        decode = DecodeAudio(srcFile,seed)

        decode.decode()
        decode.parseMsg()

        outputFile = 'decodedMsg/' + input('nama file output:') + '.' + decode.extension
        output = File(outputFile)
        byte = decode.getDecodedMsg()
        output.writeFile(byte)
    else: 
        seed = ''
        decode = DecodeAudio(srcFile,seed)

        decode.decode()
        decode.parseMsg()

        outputFile = 'decodedMsg/' + input('nama file output:') + '.' + decode.extension
        output = File(outputFile)
        byte = decode.getDecodedMsg()
        output.writeFile(byte)


# EncodeStart()
DecodeStart()