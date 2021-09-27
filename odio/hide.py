import os
import random
import extendedVigenere as ev
import wave

def decimal2Binary(number):
    return bin(number).replace("0b","")

def generateSeed(Key):
    seed = 0
    for i in range(len(Key)):
        seed += ord(Key[i])
    
    return seed

def _hide(audio_path, msg_path, dest, Key, status):
    
    # Opening audio file
    with wave.open(audio_path, "rb") as ori_wav:

        # audio metadata
        n_channels = ori_wav.getnchannels()      # 1=Mono, 2=Stereo.
        sample_width = ori_wav.getsampwidth()    # Sample width in bytes.
        framerate = ori_wav.getframerate()       # Frame rate.
        n_frames = ori_wav.getnframes()          # Number of frames.
        comp_type = ori_wav.getcomptype()        # Compression type (only supports "NONE").
        comp_name = ori_wav.getcompname()        # Compression name.

        # audio data
        frames = list(ori_wav.readframes(n_frames))  
        temp = frames.copy()
    
    # Opening message file --> bits
    filename, file_extension = os.path.splitext(msg_path)
    with open(msg_path, "rb") as f:
        message = f.read()
    if (file_extension == '.txt'):  # if the message is in txt, just encrypt it
        message = message.decode("utf-8")
        if (status):
            message = ev._encrypt(message, Key)
        bin_message = ''.join('{0:b}'.format(ord(x)).zfill(8) for x in message)
    else:   # otherwise, convert it to binary
        message = list(message)
        bin_message = ''
        for i in range(len(message)):
            bin_message += decimal2Binary(message[i])
    
    l = '{0:b}'.format(len(bin_message))
    n = 8 * (len(l)//8 + 1)
    message_length = "{0:b}".format(len(bin_message)).zfill(24) #message <= 1MB


    #Check if message length ≤ frames

    # otherwise
        # insert message into wav file

