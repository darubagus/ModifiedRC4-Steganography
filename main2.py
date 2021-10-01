import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog
from citra.Image_Stego import *
from odio.encodeOO import EncodeAudio
from odio.decodeOO import DecodeAudio
from odio.ioFile import File
from odio.PSNR import psnr
from mrc4.mrc4 import *
import cv2

#---------------------------------UTILITIES---------------------------------
def goBack():
    # widget.setCurrentIndex(widget.currentIndex() - 1)
    widget.removeWidget(widget.currentWidget())

#---------------------------------HOME---------------------------------
class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("UI/main.ui", self)

        self.pushButton.clicked.connect(self.goToRC4)
        self.pushButton_2.clicked.connect(self.goToImage)
        self.pushButton_3.clicked.connect(self.goToAudio)

    def goToImage(self):
        image = ImageScreen()
        widget.addWidget(image)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToAudio(self):
        audio = AudioScreen()
        widget.addWidget(audio)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goToRC4(self):
        rc4 = RC4Screen()
        widget.addWidget(rc4)
        widget.setCurrentIndex(widget.currentIndex()+1)
    

#---------------------------------IMAGE---------------------------------
class ImageScreen(QDialog):
    def __init__(self):
        super(ImageScreen, self).__init__()
        loadUi("UI/image/image-main.ui", self)

        self.pushButton.clicked.connect(self.goToImageEncode)
        self.pushButton_2.clicked.connect(self.goToImageDecode)
        self.backButton.clicked.connect(goBack)

    def goToImageEncode(self):
        image1 = ImageEncodeScreen()
        widget.addWidget(image1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToImageDecode(self):
        image1 = ImageDecodeScreen()
        widget.addWidget(image1)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class ImageEncodeScreen(QDialog):
    def __init__(self):
        super(ImageEncodeScreen, self).__init__()
        loadUi("UI/image/image-encode.ui", self)
        self.mode = "encode"
        self.vesselPath = ""
        self.message = ""
        self.fileInputMethod = ""
        self.outputPath = ""
        self.random = False
        self.encrypt = False
        self.seed = 0

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.insButton_1.clicked.connect(self.toggleInsButton1)
        self.insButton_2.clicked.connect(self.toggleInsButton2)
        self.encButton_1.clicked.connect(self.toggleEncButton1)
        self.encButton_2.clicked.connect(self.toggleEncButton2)
        self.goButton.clicked.connect(self.runEncoding)
        self.backButton.clicked.connect(goBack)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.png *.bmp')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)
    def toggleInsButton1(self): self.btnInsertionState(self.insButton_1)
    def toggleInsButton2(self): self.btnInsertionState(self.insButton_2)
    def toggleEncButton1(self): self.btnEncryptionState(self.encButton_1)
    def toggleEncButton2(self): self.btnEncryptionState(self.encButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)
    
    def btnEncryptionState(self, b):
        if b.text() == "Yes":
            if b.isChecked():
                self.encrypt = True
    
    def encryptMessage(self):
        if self.encrypt:
            acquire_key(self.stegoKeyField.text())
            print(f"Key: {self.stegoKeyField.text()}")
            self.message = cr4_encrypt_message(self.message)

    def getBinaryMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = file2bin(path)
        else:
            plaintext = self.inputKeyboardField.text()
            self.message = str2bin(plaintext)

    def getOutputPath(self):
        self.outputPath = "output_encode/" + self.outputFileField.text() + "." + self.outputFormatField.text()

    def getRandom(self):
        if self.insButton_2.isChecked():
            self.random = True
            self.seed = (int(''.join(map(str, map(ord, self.stegoKeyField.text()))))) % (2**32 - 1)


    def runEncoding(self):
        self.getBinaryMessage()
        self.encryptMessage()
        self.getOutputPath()
        self.getRandom()

        encode(self.message, self.vesselPath, self.outputPath, self.random, self.seed)

        original = cv2.imread(self.vesselPath)
        compressed = cv2.imread(self.outputPath, 1)
        psnrValue = PSNR(original, compressed)

        self.gotToResult(psnrValue)

    def gotToResult(self, _psnr):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        psnrValue = "PSNR: " + str(_psnr) + " dB"
        result = ImageResultScreen(self.mode, filename, psnrValue)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ImageDecodeScreen(QDialog):
    def __init__(self):
        super(ImageDecodeScreen, self).__init__()
        loadUi("UI/image/image-decode.ui", self)
        self.mode = "decode"
        self.vesselPath = ""
        self.outputPath = ""
        self.random = False
        self.decrypt = False
        self.seed = 0

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.goButton.clicked.connect(self.runDecoding)
        self.backButton.clicked.connect(goBack)
        self.encButton_1.clicked.connect(self.toggleEncButton1)
        self.encButton_2.clicked.connect(self.toggleEncButton2)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.png *.bmp')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]
    
    def toggleEncButton1(self): self.btnEncryptionState(self.encButton_1)
    def toggleEncButton2(self): self.btnEncryptionState(self.encButton_2)

    def btnEncryptionState(self, b):
        if b.text() == "Yes":
            if b.isChecked():
                self.decrypt = True
    
    def decryptMessage(self):
        if self.decrypt:
            acquire_key(self.stegoKeyField.text())
            # Decrypt output file
            cr4_decrypt_file(self.outputFileField.text(), self.outputFormatField.text())

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)

    def getRandom(self):
        if self.stegoKeyField.text() != "":
            self.random = True
            self.seed = (int(''.join(map(str, map(ord, self.stegoKeyField.text()))))) % (2**32 - 1)

    def runDecoding(self):
        self.getRandom()

        decode(self.vesselPath, self.outputFileField.text(), self.outputFormatField.text(), self.random, self.seed)
        self.decryptMessage()
        print("All decoded")
        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        pnsr = ""
        result = ImageResultScreen(self.mode, filename, pnsr)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ImageResultScreen(QDialog):
    def __init__(self, _mode, _resultFileName, _psnr):
        super(ImageResultScreen, self).__init__()
        loadUi("UI/image/image-result.ui", self)
        self.label.setText((_mode+"d").capitalize())
        self.fileNameLabel.setText(_resultFileName)
        self.psnrLabel.setText(_psnr)

        #actions
        self.goButton.clicked.connect(self.goToHome)

    def goToHome(self):
        for i in range(3):
            goBack()

#---------------------------------AUDIO---------------------------------
class AudioScreen(QDialog):
    def __init__(self):
        super(AudioScreen, self).__init__()
        loadUi("UI/audio/audio-main.ui", self)

        self.pushButton.clicked.connect(self.goToAudioEncode)
        self.pushButton_2.clicked.connect(self.goToAudioDecode)
        self.backButton.clicked.connect(goBack)

    def goToAudioEncode(self):
        audioEncode = AudioEncodeScreen()
        widget.addWidget(audioEncode)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAudioDecode(self):
        audioDecode = AudioDecodeScreen()
        widget.addWidget(audioDecode)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class AudioEncodeScreen(QDialog):
    def __init__(self):
        super(AudioEncodeScreen, self).__init__()
        loadUi("UI/audio/audio-encode.ui", self)
        self.mode = "encode"
        self.vesselPath = ""
        self.message = ""
        self.fileInputMethod = ""
        self.outputPath = ""
        self.random = False
        self.seed = 0
        self.audioEncode = ""
        self.modifiedFrame = ""

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.insButton_1.clicked.connect(self.toggleInsButton1)
        self.insButton_2.clicked.connect(self.toggleInsButton2)
        self.goButton.clicked.connect(self.runEncoding)
        self.backButton.clicked.connect(goBack)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/darubagus/Desktop', '*.wav')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/darubagus/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)
    def toggleInsButton1(self): self.btnInsertionState(self.insButton_1)
    def toggleInsButton2(self): self.btnInsertionState(self.insButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)

    def getBinaryMessage(self):
        if (self.fileInputMethod == "File"):
            self.msgPath = self.inputFileField.text()
            # msg = File(path)
            # self.message = msg.readFile()
            # self.message = file2bin(path)
        else:
            plaintext = self.inputKeyboardField.text()
            self.msgPath = 'message/message.txt'
            msg = File(self.msgPath)
            msg.writeTextFile(plaintext)
            # self.message = str2bin(plaintext)

    def getOutputPath(self):
        self.outputPath = "output_encode/" + self.outputFileField.text() + ".wav" 

    def getRandom(self):
        if self.insButton_2.isChecked():
            self.random = True
            self.seed = self.stegoKeyField.text()
        else:
            self.random = False
            self.seed = ''

    def runEncoding(self):
        self.getBinaryMessage()
        self.getOutputPath()
        self.getRandom()
        # get encrypt

        # encode(self.message, self.vesselPath, self.outputPath, self.random, self.seed)
        self.audioEncode = EncodeAudio(self.vesselPath, self.msgPath, self.seed)
        self.modifiedFrame = self.audioEncode.encodeAudio(self.random, False)
        # print(self.modifiedFrame)
        

        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + ".wav"
        path = 'output_encode/' + filename
        output = File(path)
        output.writeAudioFile(self.modifiedFrame, self.audioEncode.metadata)
        pnsr = str(psnr(self.vesselPath, self.outputPath)) + ' dB'
        result = AudioResultScreen(self.mode, filename, pnsr)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class AudioDecodeScreen(QDialog):
    def __init__(self):
        super(AudioDecodeScreen, self).__init__()
        loadUi("UI/audio/audio-decode.ui", self)
        self.mode = "decode"
        self.vesselPath = ""
        self.outputPath = ""
        self.random = False
        self.seed = 0
        self.decodeAudio = ""

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.goButton.clicked.connect(self.runDecoding)
        self.backButton.clicked.connect(goBack)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/darubagus/Desktop', '*.wav')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)

    def getRandom(self):
        if self.stegoKeyField.text() != "":
            self.random = True
            self.seed = self.stegoKeyField.text()
        else :
            self.random = False
            self.seed = ''

    def runDecoding(self):
        self.getRandom()

        # decode(self.vesselPath, self.outputFileField.text(), self.outputFormatField.text(), self.random, self.seed)
        self.decodeAudio = DecodeAudio(self.vesselPath, self.seed)
        # self.decodeAudio.decode()
        # self.decodeAudio.parseMsg()
        print("All decoded")
        self.gotToResult()

    def gotToResult(self):
        self.decodeAudio.decode()
        self.decodeAudio.parseMsg()
        filename = self.outputFileField.text() + "." + self.decodeAudio.extension
        path = 'output_decode/' + filename
        
        byte = self.decodeAudio.getDecodedMsg()
        output = File(path)
        output.writeFile(byte)

        pnsr = ""
        result = AudioResultScreen(self.mode, filename, pnsr)
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class AudioResultScreen(QDialog):
    def __init__(self, _mode, _resultFileName, _psnr):
        super(AudioResultScreen, self).__init__()
        loadUi("UI/audio/audio-result.ui", self)
        self.label.setText((_mode+"d").capitalize())
        self.fileNameLabel.setText(_resultFileName)
        self.psnrLabel.setText(_psnr)

        #actions
        self.goButton.clicked.connect(self.goToHome)

    def goToHome(self):
        for i in range(3):
            goBack()

#---------------------------------RC4---------------------------------

class RC4Screen(QDialog):
    def __init__(self):
        super(RC4Screen, self).__init__()
        loadUi("UI/RC4/rc4-main.ui", self)

        self.pushButton.clicked.connect(self.goToRC4Encrypt)
        self.pushButton_2.clicked.connect(self.goToRC4Decrypt)
        self.backButton.clicked.connect(goBack)

    def goToRC4Encrypt(self):
        rc1 = RC4EncryptScreen()
        widget.addWidget(rc1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToRC4Decrypt(self):
        rc1 = RC4DecryptScreen()
        widget.addWidget(rc1)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class RC4EncryptScreen(QDialog):
    def __init__(self):
        super(RC4EncryptScreen, self).__init__()
        loadUi("UI/RC4/rc4-encrypt.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.goButton.clicked.connect(self.runEncoding)
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = readfile_bin(path)
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "output_encode/" + self.outputFileField.text() + "." + self.outputFormatField.text()

    def runEncoding(self):
        self.getMessage()
        self.getOutputPath()
        self.key = self.stegoKeyField.text()
        acquire_key(self.key)
        result = encrypt_text(self.message)
        writefile_bin(self.outputPath, result)

        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        result = RC4ResultScreen(self.mode, filename, "")
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RC4DecryptScreen(QDialog):
    def __init__(self):
        super(RC4DecryptScreen, self).__init__()
        loadUi("UI/RC4/rc4-decrypt.ui", self)
        self.mode = "decrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.goButton.clicked.connect(self.runDecoding)
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = readfile_bin(path)
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "output_decode/" + self.outputFileField.text() + "." + self.outputFormatField.text()

    def runDecoding(self):
        self.getMessage()
        self.getOutputPath()
        self.key = self.stegoKeyField.text()
        acquire_key(self.key)
        result = decrypt_text(self.message)
        writefile_bin(self.outputPath, result)

        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        result = RC4ResultScreen(self.mode, filename, "")
        widget.addWidget(result)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RC4ResultScreen(QDialog):
    def __init__(self, _mode, _resultFileName, _psnr):
        super(RC4ResultScreen, self).__init__()
        loadUi("UI/RC4/rc4-result.ui", self)
        self.label.setText((_mode+"ed").capitalize())
        self.fileNameLabel.setText(_resultFileName)
        self.psnrLabel.setText(_psnr)

        #actions
        self.goButton.clicked.connect(self.goToHome)

    def goToHome(self):
        for i in range(3):
            goBack()

#main
app = QApplication(sys.argv)
widget = QStackedWidget()

home = HomeScreen()

widget.addWidget(home)
widget.setFixedWidth(850)
widget.setFixedHeight(600)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")