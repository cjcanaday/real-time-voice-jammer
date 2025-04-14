import sounddevice as sd
import numpy as np
from collections import deque
import argparse
import time

# Command Line Args
parser = argparse.ArgumentParser(description="Real-Time Voice Jammer")
parser.add_argument('--delay', type=float, default=0.3,
                    help='Delay in seconds (default: 0.3)')
parser.add_argument('--samplerate', type=int, default=44100,
                    help='Sample rate in Hz (default: 44100)')
parser.add_argument('--blocksize', type=int, default=2048,
                    help='Block size (default: 2048)')
parser.add_argument('--device', type=int, nargs=2, metavar=('IN', 'OUT'), default=[1,3],
                    help='Input and output device IDs (e.g. --device 1 3)')
args = parser.parse_args()

# Config Values
DELAY = args.delay
SAMPLE_RATE = args.samplerate
BLOCK_SIZE = args.blocksize
DEVICE = args.device

# Input Monitoring
SILENCE_THRESHOLD = 1e-4
SILENT_BLOCK_LIMIT = 100
silence_counter = 0

DELAY_SAMPLES = int(np.ceil(DELAY * SAMPLE_RATE / BLOCK_SIZE))
BUFFER = deque(maxlen=DELAY_SAMPLES)

def jammer(indata, outdata, frames, time, status):
    if status:
        print(status, flush=True)

    
    volume = np.linalg.norm(indata)
    if volume < SILENCE_THRESHOLD: # check if there is audio in input
        silence_counter += 1 # if no audio, keep track for how long
    else:
        silence_counter = 0

    # Store a copy of the current input block
    BUFFER.append(indata.copy())

    if len(BUFFER) == BUFFER.maxlen:
       # if buffer is full, return old audio from DELAY seconds ago
        outdata[:] = BUFFER[0]
    else:
        # if buffer isn't full, return no sound
        outdata[:] = np.zeros_like(indata)


print("Voice Jammer running")
print(f"  Delay: {DELAY}s | Sample Rate: {SAMPLE_RATE} | Block Size: {BLOCK_SIZE}")
print(f"  Using device: {DEVICE}")
print(f"  Blocks delayed: {DELAY_SAMPLES}\n")


try:
    with sd.Stream(device=DEVICE,
                   channels=1,
                   dtype='float32',
                   samplerate=SAMPLE_RATE,
                   blocksize=BLOCK_SIZE,
                   latency='high',
                   callback=jammer):
        while True:
            time.sleep(0.1)  # Keep the stream open

            if silence_counter > SILENT_BLOCK_LIMIT:
                print("No audio input detected.")
                print("Try specifying a device manually with:")
                print("   python jammer.py --device <input_id> <output_id>")


except KeyboardInterrupt:
    print("\n Stopped by user.")   

