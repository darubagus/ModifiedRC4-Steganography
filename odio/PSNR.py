import numpy as np
import math
import librosa #audio processing lib

def psnr(audio_original, audio_stego):
    ssd = 0
    ori, sr = librosa.load(audio_original)
    stego,sr = librosa.load(audio_stego)
    for i in range(len(ori)):
        ssd += np.square(ori[i] - stego[i])
    rms = np.sqrt(ssd/len(ori*stego))

    return (20 * math.log10(255/rms))

# ori = 'original/' + input("original audio:") + '.wav'
# steg = 'stego/' + input("stegano audio:") + '.wav'
# audio_original, sr = librosa.load(ori)
# audio_stego, sr2 = librosa.load(steg)

# if (len(audio_original) == len(audio_stego)):
# 	print("\n Result: " , psnr(audio_original, audio_stego) , "dB")
# else:
# 	print("\nError : faulty audio")