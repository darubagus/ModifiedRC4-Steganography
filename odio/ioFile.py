import wave

class File:
    def __init__(self, fileName):
        self.fileName = fileName
    
    def initBuffAudio(self):
        audio = wave.open(self.fileName, mode='rb')
        init_buff = audio.readframes(-1)
        init_buff = [item + 0 for item in init_buff]
        audio.close()

        return init_buff

    def readAudioFile(self):
        audio = wave.open(self.fileName, mode='rb')
        frames = bytearray(list(audio.readframes(audio.getnframes())))
        audio.close()

        return frames

    def writeAudioFile(self, frame, metadata):
        audio = wave.open(self.fileName, mode='wb')
        audio.setparams(metadata)
        audio.writeframes(frame)
        audio.close()

    def getMetadataAudio(self):
        song = wave.open(self.fileName, mode='rb')
        params = song.getparams()
        song.close()

        return params

    def getExtension(self):
        isExtension = self.fileName.split("/")[-1].find(".") != -1
        self.extension = ""

        if (isExtension):
            self.extension = self.fileName.split(".")[-1]

        return self.extension

    def readFile(self):
        with open(self.fileName, "rb") as f:
            byte_file = f.read()

        return byte_file

    def writeFile(self, bytes_file):
        with open(self.fileName, 'wb') as f:
            f.write(bytes_file)
    
    def writeTextFile(self, text):
        with open(self.fileName, 'w') as f:
            f.write(text)