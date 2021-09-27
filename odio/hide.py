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

def _hide(audio_path, msg_path, dest, Key, isEncrypted):
    
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
        if (isEncrypted):
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
    if (len(bin_message) > n_frames-25):
        print("not enough frames")
    # otherwise
    else:
        # insert message metadata into wav file
        # byte pertama menyimpan mode storing
        # 1. random->encrypted
        # 2. sequential-> not encrypted
        if (temp[0]%2 == 0) and isEncrypted:
            temp[0] += 1
        elif (temp[0]%2 == 0) and not(isEncrypted):
            temp[0] -= 1
        
        # byte ke-2 s.d 25 untuk menyimpan panjang pesan
        for i in range(1, 25):
            if ((temp[i] % 2 == 0) and (message_length[i-1] == '1')):
                temp[i] += 1
            elif ((temp[i] % 2 == 1) and (message_length[i-1] == '0')):
                temp[i] -= 1

        # Insert message content
        if (not(isEncrypted)): #then sequential
            for i in range(25,len(bin_message+25)):
                if ((temp[i]%2 == 0) and (bin_message[i-25] == '1')):
                    temp[i] += 1
                elif ((temp[i]%2 == 1) and (bin_message[i-25] == '0')):
                    temp[i] -= 1
        else: #random
            rand_i = random.sample(range(25, n_frames), len(bin_message))
            for i in range(len(bin_message)):
                if ((temp[rand_i[i]] % 2 == 0) and (bin_message[i] == '1')):
                    temp[rand_i[i]] += 1
                elif ((temp[rand_i[i]] % 2 == 1) and (bin_message[i] == '0')):
                    temp[rand_i[i]] -= 1    

        # push temp into container
        stegoFrames = bytes(temp)

        #write stego into file
        with wave.open(dest, "wb") as stegoFile:    # Open WAV file in write-only mode.
            # Write audio data.
            metadata = (n_channels, sample_width, framerate, n_frames, comp_type, comp_name)
            stegoFile.setparams(metadata)
            stegoFile.writeframes(stegoFrames)
        print("\nPesan berhasil disembunyikan")

