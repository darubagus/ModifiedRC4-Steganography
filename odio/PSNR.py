import numpy as np
import math
import librosa #audio processing lib

def psnr(audio_original, audio_stego):
    ssd = 0
    for i in range(len(audio_original)):
        ssd += np.square(audio_original[i] - audio_stego[i])
    rms = np.sqrt(ssd/len(audio_original*audio_stego))

    return (20 * math.log10(255/rms))

ori = 'original/' + input("original audio:") + '.wav'
steg = 'stego/' + input("stegano audio:") + '.wav'
audio_original, sr = librosa.load(ori)
audio_stego, sr2 = librosa.load(steg)

if (len(audio_original) == len(audio_stego)):
	print("\n Result: " , psnr(audio_original, audio_stego) , "dB")
else:
	print("\nError : faulty audio")