import wave
import random
import base64
from odio.ioFile import File

class DecodeAudio:
    def __init__(self, filePath, key):
        stegoAudio = File(filePath)
        self.key = key
        self.frames = stegoAudio.readAudioFile()

    def generateSeed(self):
        return sum([ord(k) for k in self.key]) 
    
    def getDecodedMsg(self):
        initial = len(str(self.lenMsg)) + len(str(self.extension)) + 2

        decodedMsg = self.strMsg[initial:initial + self.lenMsg]

        bytesFile = decodedMsg.encode('utf-8')
        return base64.b64decode(bytesFile)

    def parseMsg(self):
        msgInfo = self.strMsg.split('#')

        self.lenMsg = int(msgInfo[0])
        self.extension = msgInfo[1]

    def decode(self):
        isRandom = bin(self.frames[1])[-1] == '1'
        isEncrypted = bin(self.frames[0])[-1] == '1'

        self.seed = self.generateSeed()
        extracted = [self.frames[i] & 1 for i in range(len(self.frames))]

        msg = ''
        container = ''
        idx = 0
        idxMod = 8

        frameList = list(range(len(extracted)))
        if (isRandom):
            random.seed(self.seed)
            random.shuffle(frameList)
        
        for i in frameList:
            if i >= 2 :
                if idx % idxMod != (idxMod-1):
                    container += str(extracted[i])
                else:
                    container += str(extracted[i])
                    msg += chr(int(container, 2))
                    container = ''
                idx+=1
        
        if isEncrypted:
            #decrypt
            self.strMsg = msg
        else:
            self.strMsg = msg
