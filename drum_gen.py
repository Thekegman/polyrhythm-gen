import sounddevice as sd
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs = 44100
drum_files = [#"baseNsnare.wav",
              #"basedrum.wav",
              #"snareroll.wav",
              #"basedrum2.wav",
              "clap.wav",
              "clap.wav",
              #"hat.wav",
              "snare.wav",
              #"tom.wav"
              ]
drums = [[f]+list(wavfile.read(f)) for f in drum_files]

rhythms = [2,3]
beats = np.multiply.reduce(rhythms)

def balance_and_play(x, fs):
    scale = (1<<15)/np.max(np.abs(x))
    sd.play(np.array(x*scale, dtype="int16"), fs, blocking=True)
    
def balance_and_write(x, fs):
    scale = (1<<15)/np.max(np.abs(x))
    wavfile.write(r'output.wav', fs, np.array(x*scale, dtype="int16"))
    
def overlap_extend(overlap, audio1, audio2):
    new_audio = np.zeros((audio1.shape[0]+audio2.shape[0]-overlap, 2))
    new_audio[:audio1.shape[0], :] += audio1
    new_audio[-audio2.shape[0]:,:] += audio2
    return new_audio 

overlap = 2000
drum = [drums[i][2][:12000,:].astype('int64')//2 for i in range(len(rhythms))]

audio = np.array([], dtype='int64')

for i in range(beats):
    print(i, end=':')
    new = np.zeros_like(drum[0])
    for di, r in enumerate(rhythms):
        if i % r ==0:
            print(di, end=',')
            new += drum[di]
    print()
    if audio.size > 0:
        new_audio = np.zeros((audio.shape[0]+new.shape[0]-overlap, 2))
        new_audio[:audio.shape[0], :] += audio
        new_audio[-new.shape[0]:,:] += new
        audio = new_audio 
    else:
        audio = new
        
output = audio
for i in range(5):
    output = overlap_extend(overlap, output, audio)

    
balance_and_write(output, fs) 
balance_and_play(output, fs)
#plt.show()
