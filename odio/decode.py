import encode

def countSeed(key): 
    return sum([ord(i) for i in key])

def parse_message(msg):
    info = msg.split('#')
    lenMsg = int(info[0])
    MsgExtension = info[1]

    return lenMsg, MsgExtension

def getMessage(lenMsg, extension, msg):
    initial = len(str(lenMsg)) + len(str(extension)) + 2
    decoded = msg[initial:initial + lenMsg]

    byteFile = decoded.encode('utf-8')
    return encode.base64.b64decode(byteFile)

def decode(srcFile, random, *key):
    audio = encode.readAudioFile(srcFile)

    isEncrypted = bin(audio[0])[-1] == '1'
    randomFrame = bin(audio[1])[-1] == '1'

    seed = countSeed(key)
    print(seed)
    extracted = [audio[i] & 1 for i in range(len(audio))]

    idx = 0
    idxmod = 0
    msg = ''
    temp = ''

    frameList = list(range(len(extracted)))
    if randomFrame:
        encode.random.seed(seed)
        encode.random.shuffle(frameList)

    for i in frameList:
        if i >= 2:
            if idx % idxmod != (idxmod-i):
                temp+= str(extracted[i])
            else:
                temp += str(extracted[i])
                msg += chr(int(temp,2))
                temp = ''

            idx += 1

    if isEncrypted:
        #decrypt
        stringMessage= ''
    else :
        stringMessage = msg
    
    return stringMessage
    
def main():
    srcFile = 'stego/hasil1.wav'
    # srcFile = input("Masukkan path menuju file pembungkus: ")
    
    # random = input("Random or not bro? (Yes/No): ")
    random = 'Yes'
    # destFile = input("Masukkan nama untuk file hasil: ")
    # destFormat = input("Masukkan format untuk file hasil: ")

    if random == "Yes": 
        seed = input("Masukkan stego-key!: ")
        # decode(srcFile, destFile, destFormat, True, seed)
        msg = decode(srcFile, random, seed)
        lenMsg, extension = parse_message(msg)
        fileName = 'msg/'+ input("Masukkan nama file output: " + extension)
        byte = getMessage(lenMsg, extension, msg)
        encode.writeFiles(fileName, byte)
        print("Finished")
    else: 
        decode(srcFile, destFile, destFormat, False)

    

    # fileName = 'msg/'+ input("Masukkan nama file output: " + extension)
    # byte = getMessage(lenMsg, extension, msg)
    # encode.writeFiles(fileName, byte)
    # print("Finished")

    

if __name__ == '__main__':
    main()

