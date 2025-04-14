import sounddevice as sd
import numpy as np
from collections import deque

# config values
DELAY = 0.15 # seconds
SAMPLE_RATE = 44100
BLOCK_SIZE = 1024

DELAY_SAMPLES = int(np.ceil(DELAY * SAMPLE_RATE / BLOCK_SIZE))
BUFFER = deque(maxlen=DELAY_SAMPLES)

def jammer(indata, outdata, frames, time, status):
    if status:
        print(status, flush=True)

    # Store a copy of the current input block
    BUFFER.append(indata.copy())

    if len(BUFFER) == BUFFER.maxlen:
       # if buffer is full, return old audio from DELAY seconds ago
        outdata[:] = BUFFER[0]
    else:
        # if buffer isn't full, return no sound
        outdata[:] = np.zeros_like(indata)
    
try:
    with sd.Stream(device=(1,3),channels=1, dtype='float32', callback=jammer, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE):
        while True:
            pass  # Keep the stream open
except KeyboardInterrupt:
    print("\n Stopped by user.")   

