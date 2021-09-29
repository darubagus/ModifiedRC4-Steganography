import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog
from citra.Image_Stego import *

#---------------------------------UTILITIES---------------------------------
def goBack():
    # widget.setCurrentIndex(widget.currentIndex() - 1)
    widget.removeWidget(widget.currentWidget())

#---------------------------------HOME---------------------------------
class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("UI/main.ui", self)

        self.pushButton_2.clicked.connect(self.goToImage)

    def goToImage(self):
        image = ImageScreen()
        widget.addWidget(image)
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
        self.seed = 0

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
            self.seed = int(self.stegoKeyField.text())


    def runEncoding(self):
        self.getBinaryMessage()
        self.getOutputPath()
        self.getRandom()

        encode(self.message, self.vesselPath, self.outputPath, self.random, self.seed)
        self.gotToResult()

    def gotToResult(self):
        filename = self.outputFileField.text() + "." + self.outputFormatField.text()
        pnsr = "PSNR: Belom buat"
        result = ImageResultScreen(self.mode, filename, pnsr)
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
        self.seed = 0

        #actions
        self.vesselButton.clicked.connect(self.browseVessel)
        self.insButton_1.clicked.connect(self.toggleInsButton1)
        self.insButton_2.clicked.connect(self.toggleInsButton2)
        self.goButton.clicked.connect(self.runDecoding)
        self.backButton.clicked.connect(goBack)

    def browseVessel(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/shifa/Desktop', '*.png *.bmp')
        self.vesselField.setText(f[0])
        self.vesselPath = f[0]

    def toggleInsButton1(self): self.btnInsertionState(self.insButton_1)
    def toggleInsButton2(self): self.btnInsertionState(self.insButton_2)

    def btnInsertionState(self, b):
        if b.text() == "Sequential":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(True)
                self.stegoKeyField.setText("")
        elif b.text() == "Random":
            if b.isChecked():
                self.stegoKeyField.setReadOnly(False)

    def getRandom(self):
        if self.insButton_2.isChecked():
            self.random = True
            self.seed = int(self.stegoKeyField.text())

    def runDecoding(self):
        self.getRandom()

        decode(self.vesselPath, self.outputFileField.text(), self.outputFormatField.text(), self.random, self.seed)
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