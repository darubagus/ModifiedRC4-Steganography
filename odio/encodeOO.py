import wave
import random
import base64
from odio.ioFile import File

class EncodeAudio:
    def __init__(self, filePath, messagePath, key):
        self.key = key
        
        audio = File(filePath)

        self.frames = audio.readAudioFile()
        self.initBuff = audio.initBuffAudio()
        self.metadata = audio.getMetadataAudio()

        msg = File(messagePath)
        self.extension = msg.getExtension()
        self.strMsg = ''
        byteMessage = msg.readFile()
        self.encodedMsg = base64.b64encode(byteMessage).decode('utf-8')
    
    def generateSeed(self):
        return sum([ord(k) for k in self.key])
    
    def randomizeFrame(self, isRandom):
        if isRandom:
            sign = 1
        else:
            sign = 0

        self.frames[1] = self.frames[1] & 254|sign
        if isRandom:
            random.seed(self.seed)
            random.shuffle(self.frameList)
    
    def encryptedMsg(self, isEncryped, key):
        if isEncryped:
            sign = 1
        else:
            sign = 0

        self.frames[0] = self.frames[0] & 254|sign

        # Ini ntar encrypt pake RC4 nya
        # if isEncryped:
        #     self.strMsg = encrypt

    def modFrame(self, arrayOfBit):
        idx=0
        for i in self.frameList:
            if idx >= len(arrayOfBit):
                break
            if i >= 2:
                self.frames[i] = self.frames[i]&254|arrayOfBit[idx]
                idx += 1
    
    def encodeAudio(self, isRandom, isEncrypted):
        self.seed = self.generateSeed()

        lenMsg = str(len(self.encodedMsg) + len(self.extension) + 2)
        # storing msg content and its info
        self.strMsg = lenMsg + '#' + self.extension + '#' + self.encodedMsg
        self.encryptedMsg(isEncrypted, self.key)

        if len(self.strMsg) > (len(self.frames) * 0.9) // 8:
            print("Message is too large")
        
        bit = map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in self.strMsg]))
        arrBits = list(bit)

        self.frameList = list(range(len(self.frames)))
        self.randomizeFrame(isRandom)
        self.modFrame(arrBits)

        return bytes(self.frames)
