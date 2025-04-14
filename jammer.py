import sounddevice as sd
import numpy as np
from collections import deque

# config values
DELAY = 0.3 # seconds
SAMPLE_RATE = 44100
BLOCK_SIZE = 1024

DELAY_SAMPLES = int(DELAY * SAMPLE_RATE)
BUFFER = deque(maxlen=DELAY_SAMPLES)

def jammer(indata, outdata, frames, time, status):
    if(status):
        print(status)

    for i in range(len(indata)):
        BUFFER.append(indata[i].copy())
        if(len(BUFFER) == BUFFER.maxlen):
            outdata[i] = BUFFER[0] # if buffer is full, return old audio from DELAY seconds ago
        else:
            outdata[i] = np.zeros_like(indata[i]) # if buffer isn't full, return no sound
    
try:
    with sd.Stream(channels=1, callback=jammer, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE):
        while True:
            pass  # Keep the stream open
except KeyboardInterrupt:
    print("\n Stopped by user.")   

